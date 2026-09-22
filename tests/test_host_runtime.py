"""Exercise packaged helpers through Python, without a terminal or API key."""
import json
import runpy
import shutil
import sys
from pathlib import Path

from conftest_ad_brainstorm import build_analysis, build_concepts


SKILLS = Path(__file__).resolve().parents[1] / "plugins/codex-ad/skills"


def test_campaign_brief_is_available_in_installed_skill():
    assert (SKILLS / "ad-maker/examples/campaign-brief.md").is_file()


def test_brainstorm_python_tool_keeps_validation_gates(tmp_path):
    skill = tmp_path / "ad-brainstorm"
    shutil.copytree(SKILLS / "ad-brainstorm", skill)
    analysis = tmp_path / "analysis.json"
    concepts = tmp_path / "concepts.json"
    analysis.write_text(json.dumps(build_analysis()))
    concepts.write_text(json.dumps(build_concepts()))
    validate_analysis = runpy.run_path(str(skill / "scripts/validate_analysis.py"))["validate"]
    validate_concepts = runpy.run_path(str(skill / "scripts/validate_concepts.py"))["validate"]
    render = runpy.run_path(str(skill / "scripts/render_concepts.py"))["render"]
    assert validate_analysis(str(analysis), 75)["passed"]
    assert validate_concepts(str(concepts), str(analysis), 75)["passed"]
    markdown = render(json.loads(concepts.read_text()))
    assert markdown.count("### F") == 100
    invalid = build_analysis()
    del invalid["rollup"]["ugc_opportunity"]
    analysis.write_text(json.dumps(invalid))
    assert not validate_analysis(str(analysis), 75)["passed"]


def test_maker_python_tool_compiles_and_scores_without_credentials(tmp_path, monkeypatch, capsys):
    skill = tmp_path / "ad-maker"
    shutil.copytree(SKILLS / "ad-maker", skill)
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    examples = skill / "references/examples"
    output = tmp_path / "prompt.json"
    script = skill / "scripts/compile_prompt.py"
    args = [str(script)]
    for name in ("brand", "product", "persona", "scenario"):
        args.extend(["--" + name, str(examples / (name + ".yaml"))])
    args.extend([
        "--mode", "brief", "--platform-preset", "meta-feed-conversion",
        "--variant-count", "1", "--headline", "Simple dinners",
        "--subline", "For busy cooks", "--offer", "Save 20%",
        "--visual", "Kitchen scene with warm lighting for busy cooks.",
        "--layout", 'Product foreground at 22%; headline "Simple dinners" and offer "Save 20%" inside safe zones.',
        "--out", str(output),
    ])
    monkeypatch.setattr(sys, "argv", args)
    assert runpy.run_path(str(script))["main"]() == 0
    prompt = json.loads(output.read_text())
    assert prompt["metadata"]["variant_count"] == 1
    assert all(Path(ref["path"]).is_file() for ref in prompt["image_refs"])
    score = runpy.run_path(str(skill / "scripts/score_prompt.py"))["score_prompt"](prompt)
    assert score["overall_score"] >= 75
    assert len(score["scores"]) == 9
    generator = skill / "scripts/generate_image.py"
    monkeypatch.setattr(sys, "argv", [str(generator), "--prompt-json", str(output),
                                      "--out-dir", str(tmp_path / "images"), "--mode", "edit", "--dry-run"])
    assert runpy.run_path(str(generator))["main"]() == 0
    request = json.loads(capsys.readouterr().out)
    assert request["endpoint"] == "images.edit"
    assert request["api_request"]["image"] == [ref["path"] for ref in prompt["image_refs"]]
    assert prompt["negative_prompt"] in request["api_request"]["prompt"]
