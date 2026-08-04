import json
import subprocess
import sys
from pathlib import Path

from conftest_ad_brainstorm import build_concepts


ROOT = Path(__file__).resolve().parents[1]
RENDER = ROOT / "plugins/codex-ad/skills/ad-brainstorm/scripts/render_concepts.py"


def render(tmp_path, concepts):
    concepts_path = tmp_path / "concepts.json"
    out_path = tmp_path / "nested" / "concepts.md"
    concepts_path.write_text(json.dumps(concepts))
    proc = subprocess.run(
        [sys.executable, str(RENDER), "--concepts", str(concepts_path), "--out", str(out_path)],
        capture_output=True, text=True,
    )
    return proc, out_path


def test_renders_all_concepts_grouped_by_format(tmp_path):
    proc, out_path = render(tmp_path, build_concepts())
    assert proc.returncode == 0, proc.stderr
    text = out_path.read_text()

    assert "# Ad Concepts - Lumora Vitamin C Brightening Serum" in text
    assert "**Grid:** 10 formats x 10 angles = 100 concepts" in text
    assert "## F1 - UGC monologue" in text
    assert "## F10 - ASMR product moment" in text
    assert text.count("**Hook:**") == 100
    assert text.count("**Platform:**") == 100
    assert "`rollup.ugc_opportunity`" in text


def test_summary_beats_stay_on_separate_rendered_lines(tmp_path):
    _, out_path = render(tmp_path, build_concepts())
    text = out_path.read_text()
    # First beat carries a markdown hard break so it does not merge with the second.
    assert "Opening beat 1 establishes the scene and the tension quickly.  \n" in text
    assert "Closing beat 1 lands the product and the argument cleanly.\n" in text


def test_creates_missing_output_directory(tmp_path):
    _, out_path = render(tmp_path, build_concepts())
    assert out_path.exists()
    assert out_path.parent.name == "nested"


def test_empty_format_row_is_marked(tmp_path):
    concepts = build_concepts()
    concepts["concepts"] = [c for c in concepts["concepts"] if c["format_index"] != 4]
    proc, out_path = render(tmp_path, concepts)
    assert proc.returncode == 0
    assert "_No concepts generated for this format._" in out_path.read_text()


def test_missing_file_exits_nonzero(tmp_path):
    proc = subprocess.run(
        [sys.executable, str(RENDER), "--concepts", str(tmp_path / "nope.json"),
         "--out", str(tmp_path / "out.md")],
        capture_output=True, text=True,
    )
    assert proc.returncode == 1
    assert "Missing file" in proc.stderr
