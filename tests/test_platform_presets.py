import json
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
COMPILE = ROOT / "plugins/ad-maker/skills/ad-maker/scripts/compile_prompt.py"
PRESETS = ROOT / "plugins/ad-maker/skills/ad-maker/references/platform-presets.yaml"
EXAMPLES = ROOT / "plugins/ad-maker/skills/ad-maker/references/examples"


def base_compile_args(tmp_path):
    return [
        sys.executable,
        str(COMPILE),
        "--brand",
        str(EXAMPLES / "brand.yaml"),
        "--product",
        str(EXAMPLES / "product.yaml"),
        "--persona",
        str(EXAMPLES / "persona.yaml"),
        "--scenario",
        str(EXAMPLES / "scenario.yaml"),
        "--mode",
        "brief",
        "--objective",
        "Conversion",
        "--variant-count",
        "4",
        "--headline",
        "Simple dinners, better flavor",
        "--subline",
        "Chef-level sauce for busy weeknights",
        "--offer",
        "Save 20% today",
        "--out",
        str(tmp_path / "prompt.json"),
    ]


def test_platform_presets_define_marketer_channels():
    data = yaml.safe_load(PRESETS.read_text())
    assert data["meta-feed-conversion"]["ratio"] == "4:5"
    assert data["instagram-story"]["ratio"] == "9:16"
    assert data["square-retargeting"]["ratio"] == "1:1"
    assert data["tiktok-static"]["ratio"] == "9:16"
    assert data["linkedin-lead-gen"]["ratio"] == "1:1"
    for preset in data.values():
        assert preset["layout_guidance"]
        assert preset["creative_style"]


def test_compile_prompt_uses_platform_preset_ratio_and_layout(tmp_path):
    output = tmp_path / "prompt.json"
    args = base_compile_args(tmp_path)
    args[args.index(str(output))] = str(output)
    args.extend(["--platform-preset", "instagram-story"])

    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)

    assert result.returncode == 0, result.stderr
    data = json.loads(output.read_text())
    assert data["metadata"]["platform_preset"] == "instagram-story"
    assert data["metadata"]["ratio"] == "9:16"
    assert data["metadata"]["size"] == "1152x2048"
    assert "vertical safe zone" in data["prompt"]


def test_compile_prompt_rejects_unknown_platform_preset(tmp_path):
    args = base_compile_args(tmp_path)
    args.extend(["--platform-preset", "unknown-channel"])
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)

    assert result.returncode != 0
    assert "Unsupported platform preset" in result.stderr
