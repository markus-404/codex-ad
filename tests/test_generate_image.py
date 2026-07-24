import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins/ad-maker/skills/ad-maker/scripts/generate_image.py"


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
    assert payload["model"] == "gpt-image-2"
    assert payload["size"] == "1024x1024"
    assert payload["n"] == 1


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
