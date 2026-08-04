import json
import subprocess
import sys
from pathlib import Path

from conftest_ad_brainstorm import build_analysis


ROOT = Path(__file__).resolve().parents[1]
VALIDATE = ROOT / "plugins/codex-ad/skills/ad-brainstorm/scripts/validate_analysis.py"


def run(tmp_path, analysis, extra=None):
    path = tmp_path / "analysis.json"
    path.write_text(json.dumps(analysis))
    cmd = [sys.executable, str(VALIDATE), "--analysis", str(path)] + (extra or [])
    proc = subprocess.run(cmd, capture_output=True, text=True)
    payload = json.loads(proc.stdout) if proc.stdout.strip() else {}
    return proc.returncode, payload


def test_valid_analysis_passes(tmp_path):
    code, result = run(tmp_path, build_analysis())
    assert code == 0, result
    assert result["passed"] is True
    assert result["errors"] == []
    assert result["score"] >= 75


def test_missing_rollup_field_fails(tmp_path):
    analysis = build_analysis()
    del analysis["rollup"]["ugc_opportunity"]
    code, result = run(tmp_path, analysis)
    assert code == 1
    assert any("rollup.ugc_opportunity" in e for e in result["errors"])


def test_one_word_prose_fails(tmp_path):
    analysis = build_analysis()
    analysis["images"][0]["lighting"] = "bright"
    code, result = run(tmp_path, analysis)
    assert code == 1
    assert any("images[0].lighting" in e and "words" in e for e in result["errors"])


def test_placeholder_text_fails(tmp_path):
    analysis = build_analysis()
    analysis["rollup"]["brand_aesthetic_read"] = "TODO fill in the brand read later on"
    code, result = run(tmp_path, analysis)
    assert code == 1
    assert any("placeholder" in e for e in result["errors"])


def test_bad_hex_fails(tmp_path):
    analysis = build_analysis()
    analysis["rollup"]["color_palette"] = ["#f4ede3", "cream", "#fff"]
    code, result = run(tmp_path, analysis)
    assert code == 1
    assert any("hex" in e for e in result["errors"])


def test_identical_image_reads_fail(tmp_path):
    analysis = build_analysis()
    first = analysis["images"][0]
    for image in analysis["images"]:
        image["shot_type"] = first["shot_type"]
        image["camera_angle"] = first["camera_angle"]
        image["lighting"] = first["lighting"]
    code, result = run(tmp_path, analysis)
    assert code == 1
    assert any("analyzed individually" in e for e in result["errors"])


def test_no_humans_without_flagged_gap_fails(tmp_path):
    analysis = build_analysis()
    analysis["rollup"]["ugc_opportunity"] = "the packaging could be shown opening slowly in close macro detail"
    analysis["rollup"]["whats_missing"] = [
        "no outdoor daylight setting",
        "no scale reference object nearby",
        "no ingredient texture swatch",
        "no seasonal styling variation",
    ]
    code, result = run(tmp_path, analysis)
    assert code == 1
    assert any("gap analysis was skipped" in e for e in result["errors"])


def test_wrong_style_count_fails(tmp_path):
    analysis = build_analysis()
    analysis["rollup"]["suggested_visual_styles"] = ["only one direction here"]
    code, result = run(tmp_path, analysis)
    assert code == 1
    assert any("suggested_visual_styles" in e for e in result["errors"])


def test_invalid_enum_fails(tmp_path):
    analysis = build_analysis()
    analysis["rollup"]["packaging_style"] = "sparkly"
    code, result = run(tmp_path, analysis)
    assert code == 1
    assert any("packaging_style" in e for e in result["errors"])


def test_too_few_images_warns_but_can_pass(tmp_path):
    code, result = run(tmp_path, build_analysis(image_count=2), extra=["--min-score", "0"])
    assert code == 0
    assert any("3+" in w for w in result["warnings"])


def test_score_gate_blocks_thin_analysis(tmp_path):
    code, result = run(tmp_path, build_analysis(image_count=1), extra=["--min-score", "95"])
    assert code == 1
    assert any("below --min-score" in e for e in result["errors"])
