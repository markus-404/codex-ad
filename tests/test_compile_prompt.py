import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins/ad-maker/skills/ad-maker/scripts/compile_prompt.py"
EXAMPLES = ROOT / "plugins/ad-maker/skills/ad-maker/references/examples"


def run_compile(tmp_path, extra_args=None):
    output = tmp_path / "prompt.json"
    args = [
        sys.executable,
        str(SCRIPT),
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
        "--ratio",
        "4:5",
        "--variant-count",
        "4",
        "--headline",
        "Simple dinners, better flavor",
        "--subline",
        "Chef-level sauce for busy weeknights",
        "--offer",
        "Save 20% today",
        "--out",
        str(output),
    ]
    if extra_args:
        args.extend(extra_args)
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    return result, output


def test_compile_prompt_writes_six_slots_in_order(tmp_path):
    result, output = run_compile(tmp_path)
    assert result.returncode == 0, result.stderr
    data = json.loads(output.read_text())
    slots = ["- Visual:", "- Color:", "- Layout:", "- Text:", "- Fonts:", "- Logo:"]
    positions = [data["prompt"].index(slot) for slot in slots]
    assert positions == sorted(positions)
    assert data["metadata"]["ratio"] == "4:5"
    assert data["metadata"]["size"] == "1024x1280"
    assert data["metadata"]["variant_count"] == 4
    assert data["image_refs"][0]["role"] == "logo"
    assert data["image_refs"][1]["role"] == "product"


def test_compile_prompt_rejects_invalid_ratio(tmp_path):
    result, _ = run_compile(tmp_path, ["--ratio", "3:2"])
    assert result.returncode != 0
    assert "Unsupported ratio" in result.stderr


def test_compile_prompt_records_refinement_metadata(tmp_path):
    source_result, source_output = run_compile(tmp_path)
    assert source_result.returncode == 0, source_result.stderr
    refined_output = tmp_path / "refined.json"
    args = [
        sys.executable,
        str(SCRIPT),
        "--source-prompt-json",
        str(source_output),
        "--refine-mode",
        "layout",
        "--edit-instruction",
        "Move the offer badge closer to the product",
        "--out",
        str(refined_output),
    ]
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    data = json.loads(refined_output.read_text())
    assert data["metadata"]["lineage"]["refine_mode"] == "layout"
    assert data["metadata"]["lineage"]["source_prompt_json"] == str(source_output)
    assert "Move the offer badge closer to the product" in data["prompt"]
