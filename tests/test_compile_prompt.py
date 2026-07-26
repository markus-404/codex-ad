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


def test_compile_prompt_uses_authored_visual_and_layout(tmp_path):
    visual = "Two friends laugh over a shared bowl of pasta as steam rises in late golden light."
    layout = "Product sits low-right on the diagonal, occupying at least 18% of canvas, headline \"Simple dinners, better flavor\" stacked upper-left against negative space."
    result, output = run_compile(tmp_path, ["--visual", visual, "--layout", layout])
    assert result.returncode == 0, result.stderr
    data = json.loads(output.read_text())
    assert f"- Visual: {visual}" in data["prompt"]
    assert f"- Layout: {layout}" in data["prompt"]
    slots = ["- Visual:", "- Color:", "- Layout:", "- Text:", "- Fonts:", "- Logo:"]
    positions = [data["prompt"].index(slot) for slot in slots]
    assert positions == sorted(positions)
    assert 'Headline "Simple dinners, better flavor"' in data["prompt"]


def test_compile_prompt_falls_back_to_template_slots(tmp_path):
    result, output = run_compile(tmp_path)
    assert result.returncode == 0, result.stderr
    data = json.loads(output.read_text())
    assert "- Visual: A clean kitchen counter in warm morning light" in data["prompt"]
    assert "- Layout: Place uploaded product #1 as the central visual" in data["prompt"]


def test_compile_prompt_resolves_ref_paths_to_existing_files(tmp_path):
    # Run from an unrelated cwd to prove paths are absolute, not cwd-relative.
    result, output = run_compile(tmp_path)
    assert result.returncode == 0, result.stderr
    data = json.loads(output.read_text())
    for ref in data["image_refs"]:
        ref_path = Path(ref["path"])
        assert ref_path.is_absolute(), ref["path"]
        assert ref_path.exists(), ref["path"]


def test_compile_prompt_rejects_zero_variant_count(tmp_path):
    result, _ = run_compile(tmp_path, ["--variant-count", "0"])
    assert result.returncode != 0
    assert "--variant-count must be at least 1" in result.stderr


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
