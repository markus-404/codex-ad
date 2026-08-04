import json
import subprocess
import sys
from pathlib import Path

from conftest_ad_brainstorm import FORMATS, build_analysis, build_concepts


ROOT = Path(__file__).resolve().parents[1]
VALIDATE = ROOT / "plugins/codex-ad/skills/ad-brainstorm/scripts/validate_concepts.py"


def run(tmp_path, concepts, analysis=None, extra=None):
    concepts_path = tmp_path / "concepts.json"
    analysis_path = tmp_path / "analysis.json"
    concepts_path.write_text(json.dumps(concepts))
    analysis_path.write_text(json.dumps(analysis or build_analysis()))
    cmd = [
        sys.executable, str(VALIDATE),
        "--concepts", str(concepts_path),
        "--analysis", str(analysis_path),
    ] + (extra or [])
    proc = subprocess.run(cmd, capture_output=True, text=True)
    payload = json.loads(proc.stdout) if proc.stdout.strip() else {}
    return proc.returncode, payload


def test_full_valid_grid_passes(tmp_path):
    code, result = run(tmp_path, build_concepts())
    assert code == 0, result
    assert result["passed"] is True
    assert result["expected_cells"] == 100
    assert result["valid_concepts"] == 100


def test_missing_cell_fails(tmp_path):
    concepts = build_concepts()
    concepts["concepts"] = [c for c in concepts["concepts"] if c["id"] != "F7-A3"]
    code, result = run(tmp_path, concepts)
    assert code == 1
    assert any("F7-A3" in e for e in result["errors"])


def test_duplicate_cell_fails(tmp_path):
    concepts = build_concepts()
    concepts["concepts"].append(dict(concepts["concepts"][0]))
    code, result = run(tmp_path, concepts)
    assert code == 1
    assert any("duplicate cell F1-A1" in e for e in result["errors"])


def test_id_not_matching_cell_fails(tmp_path):
    concepts = build_concepts()
    concepts["concepts"][12]["id"] = "F9-A9"
    code, result = run(tmp_path, concepts)
    assert code == 1
    assert any("does not match its cell" in e for e in result["errors"])


def test_format_label_mismatch_fails(tmp_path):
    concepts = build_concepts()
    concepts["concepts"][5]["format"] = "Wrong archetype name"
    code, result = run(tmp_path, concepts)
    assert code == 1
    assert any("does not match grid.formats" in e for e in result["errors"])


def test_duplicate_hook_fails(tmp_path):
    concepts = build_concepts()
    concepts["concepts"][40]["hook"] = concepts["concepts"][3]["hook"]
    code, result = run(tmp_path, concepts)
    assert code == 1
    assert any("duplicate of F1-A4" in e for e in result["errors"])


def test_hook_over_word_limit_fails(tmp_path):
    concepts = build_concepts()
    concepts["concepts"][0]["hook"] = " ".join("word{0}".format(i) for i in range(16))
    code, result = run(tmp_path, concepts)
    assert code == 1
    assert any("limit is 15" in e for e in result["errors"])


def test_unresolvable_grounding_fails(tmp_path):
    concepts = build_concepts()
    concepts["concepts"][2]["visual_grounding"] = ["rollup.does_not_exist"]
    code, result = run(tmp_path, concepts)
    assert code == 1
    assert any("does not resolve" in e for e in result["errors"])


def test_out_of_range_grounding_index_fails(tmp_path):
    concepts = build_concepts()
    concepts["concepts"][4]["visual_grounding"] = ["rollup.suggested_visual_styles[99]"]
    code, result = run(tmp_path, concepts)
    assert code == 1
    assert any("does not resolve" in e for e in result["errors"])


def test_empty_grounding_fails(tmp_path):
    concepts = build_concepts()
    concepts["concepts"][6]["visual_grounding"] = []
    code, result = run(tmp_path, concepts)
    assert code == 1
    assert any("non-empty list of analysis paths" in e for e in result["errors"])


def test_bad_platform_fails(tmp_path):
    concepts = build_concepts()
    concepts["concepts"][8]["platform"] = "Snapchat"
    code, result = run(tmp_path, concepts)
    assert code == 1
    assert any("Snapchat" in e for e in result["errors"])


def test_summary_must_be_two_lines(tmp_path):
    concepts = build_concepts()
    concepts["concepts"][9]["summary"] = ["Only a single line of summary here right now."]
    code, result = run(tmp_path, concepts)
    assert code == 1
    assert any("exactly 2 lines" in e for e in result["errors"])


def test_skip_formats_shrinks_expected_grid(tmp_path):
    concepts = build_concepts(formats=FORMATS[:8])
    code, result = run(tmp_path, concepts)
    assert code == 0, result
    assert result["expected_cells"] == 80
    assert result["valid_concepts"] == 80


def test_recycled_visual_styles_drag_score_down(tmp_path):
    concepts = build_concepts()
    for concept in concepts["concepts"]:
        concept["visual_style"] = "One single recycled visual treatment everywhere"
    code, result = run(tmp_path, concepts)
    assert code == 1
    assert result["components"]["visual_variety"] < 20
    assert any("below --min-score" in e for e in result["errors"])


def test_single_grounding_path_collapses_coverage(tmp_path):
    concepts = build_concepts()
    for concept in concepts["concepts"]:
        concept["visual_grounding"] = ["rollup.ugc_opportunity"]
    code, result = run(tmp_path, concepts)
    assert code == 1
    assert result["components"]["grounding_coverage"] < 20
    assert result["components"]["grounding_depth"] == 0


def test_near_duplicate_hooks_lower_distinctness(tmp_path):
    concepts = build_concepts()
    for concept in concepts["concepts"]:
        concept["hook"] = "This serum stops pilling under SPF number {0}".format(
            concept["id"]
        )
    code, result = run(tmp_path, concepts)
    assert result["components"]["hook_distinctness"] < 100
