from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins/codex-ad/skills/ad-maker"


def test_sku_gallery_library_reference_exists_and_is_linked():
    skill_md = (SKILL / "SKILL.md").read_text()
    reference = SKILL / "references/sku-gallery-library.md"

    assert reference.exists()
    assert "references/sku-gallery-library.md" in skill_md
    assert "production" in skill_md.lower()
    assert "gallery" in skill_md.lower()
    assert "score_prompt.py" in skill_md
    assert "normal gate" in skill_md.lower()


def test_sku_gallery_library_defines_four_to_six_prompt_slots():
    text = (SKILL / "references/sku-gallery-library.md").read_text().lower()

    assert "4-6" in text
    assert "shopee" in text
    for required in [
        "slot purpose",
        "visual",
        "layout",
        "copy",
        "negative prompt",
        "reference image order",
        "readiness score",
        "output qa notes",
        "refinement instruction",
    ]:
        assert required in text


def test_refinement_workflows_include_post_generation_qa_categories():
    text = (SKILL / "references/refinement-workflows.md").read_text().lower()

    assert "post-generation qa" in text
    for required in [
        "packaging fidelity",
        "mobile text readability",
        "platform layout consistency",
        "claim risk",
        "brand tone",
    ]:
        assert required in text
