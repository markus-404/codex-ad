import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCORE = ROOT / "plugins/ad-maker/skills/ad-maker/scripts/score_prompt.py"


def write_prompt(tmp_path, prompt, negative_prompt="", image_refs=None, metadata=None):
    path = tmp_path / "prompt.json"
    path.write_text(json.dumps({
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "image_refs": image_refs if image_refs is not None else [
            {"index": 0, "role": "logo", "path": "/tmp/logo.png"},
            {"index": 1, "role": "product", "path": "/tmp/product.png"},
        ],
        "metadata": metadata or {
            "ratio": "4:5",
            "platform_preset": "meta-feed-conversion",
            "objective": "Conversion",
        },
    }))
    return path


def test_score_prompt_outputs_deterministic_rubric(tmp_path):
    prompt_json = write_prompt(
        tmp_path,
        "\n".join([
            "- Visual: Busy home cook plating pasta with the product bottle in foreground and a clear visual hook.",
            "- Color: Use #337AB7 and #FFFFFF.",
            "- Layout: Product occupies at least 18% of canvas; headline \"Simple dinners\" at top and offer \"Save 20% today\" near product.",
            "- Text: Headline \"Simple dinners\"; subline \"Chef-level sauce\"; offer \"Save 20% today\".",
            "- Fonts: Use Cormorant Garamond regular and Bricolage Grotesque regular.",
            "- Logo: Place uploaded logo #0 at top left.",
        ]),
        "- No garbled typography.\n- Do not alter product shape.",
    )

    result = subprocess.run(
        [sys.executable, str(SCORE), "--prompt-json", str(prompt_json)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["overall_score"] >= 80
    assert data["scores"]["product_prominence"] == 10
    assert data["scores"]["platform_fit"] >= 8
    assert data["risks"] == []


def test_score_prompt_flags_missing_product_and_offer(tmp_path):
    prompt_json = write_prompt(
        tmp_path,
        "- Visual: Abstract background.\n- Text: Headline \"Nice dinner\".",
        image_refs=[],
        metadata={"ratio": "1:1", "platform_preset": "meta-feed-conversion", "objective": "Conversion"},
    )

    result = subprocess.run(
        [sys.executable, str(SCORE), "--prompt-json", str(prompt_json)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["overall_score"] < 70
    assert "Missing product reference image." in data["risks"]
    assert any("offer" in item.lower() for item in data["recommendations"])
