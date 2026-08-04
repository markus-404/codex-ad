import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins/codex-ad/skills/ad-maker/scripts/generate_image.py"


def test_generate_image_dry_run_prints_payload(tmp_path):
    prompt_json = tmp_path / "prompt.json"
    prompt_json.write_text(json.dumps({
        "prompt": "- Visual: Test scene\n- Color: #337AB7\n- Layout: Centered product\n- Text: Headline \"Test\"\n- Fonts: Inter regular\n- Logo: uploaded logo #0 top left",
        "negative_prompt": "- No garbled typography",
        "image_refs": [],
        "metadata": {
            "ratio": "1:1",
            "size": "1024x1024",
            "variant_count": 1
        }
    }))
    args = [
        sys.executable,
        str(SCRIPT),
        "--prompt-json",
        str(prompt_json),
        "--count",
        "1",
        "--ratio",
        "1:1",
        "--out-dir",
        str(tmp_path / "images"),
        "--dry-run",
    ]
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    request = payload["api_request"]
    assert payload["endpoint"] == "images.generate"
    assert request["model"] == "gpt-image-2"
    assert request["size"] == "1024x1024"
    assert request["quality"] == "medium"
    assert request["n"] == 1
    # negative_prompt is not an API param; it is folded into the prompt text.
    assert "negative_prompt" not in request
    assert "Avoid the following:" in request["prompt"]
    assert "No garbled typography" in request["prompt"]


def test_generate_image_uses_prompt_metadata_defaults(tmp_path):
    prompt_json = tmp_path / "prompt.json"
    prompt_json.write_text(json.dumps({
        "prompt": "- Visual: Test scene",
        "negative_prompt": "",
        "image_refs": [],
        "metadata": {"ratio": "4:5", "size": "1024x1280", "variant_count": 3},
    }))
    args = [
        sys.executable,
        str(SCRIPT),
        "--prompt-json",
        str(prompt_json),
        "--out-dir",
        str(tmp_path / "images"),
        "--dry-run",
    ]
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    request = json.loads(result.stdout)["api_request"]
    assert request["size"] == "1024x1280"
    assert request["n"] == 3


def test_generate_image_rejects_zero_count(tmp_path):
    prompt_json = tmp_path / "prompt.json"
    prompt_json.write_text(json.dumps({
        "prompt": "- Visual: Test scene",
        "negative_prompt": "",
        "image_refs": [],
        "metadata": {"ratio": "1:1", "size": "1024x1024", "variant_count": 1},
    }))
    args = [
        sys.executable,
        str(SCRIPT),
        "--prompt-json",
        str(prompt_json),
        "--count",
        "0",
        "--ratio",
        "1:1",
        "--out-dir",
        str(tmp_path / "images"),
        "--dry-run",
    ]
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    assert result.returncode != 0
    assert "--count must be between 1 and 10" in result.stderr


def test_generate_image_requires_key_without_dry_run(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    prompt_json = tmp_path / "prompt.json"
    prompt_json.write_text(json.dumps({
        "prompt": "- Visual: Test scene\n- Color: #337AB7\n- Layout: Centered product\n- Text: Headline \"Test\"\n- Fonts: Inter regular\n- Logo: uploaded logo #0 top left",
        "negative_prompt": "- No garbled typography",
        "image_refs": [],
        "metadata": {
            "ratio": "1:1",
            "size": "1024x1024",
            "variant_count": 1
        }
    }))
    args = [
        sys.executable,
        str(SCRIPT),
        "--prompt-json",
        str(prompt_json),
        "--count",
        "1",
        "--ratio",
        "1:1",
        "--out-dir",
        str(tmp_path / "images"),
    ]
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    assert result.returncode != 0
    assert "OPENAI_API_KEY is required unless --dry-run is set." in result.stderr
