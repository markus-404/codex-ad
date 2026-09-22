import re
from pathlib import Path

import yaml


SKILL = Path(__file__).resolve().parents[1] / "plugins/codex-ad/skills/ad-maker2"


def test_ad_maker2_requires_explicit_codex_invocation():
    metadata = yaml.safe_load((SKILL / "agents/openai.yaml").read_text())
    assert metadata["policy"]["allow_implicit_invocation"] is False
    assert "$ad-maker2" in metadata["interface"]["default_prompt"]


def test_ad_maker2_local_references_resolve_inside_installed_plugin():
    plugin = SKILL.parent.parent.resolve()
    documents = [SKILL / "SKILL.md", *SKILL.glob("references/*.md")]
    assert documents[0].is_file()
    for document in documents:
        for target in re.findall(r"\]\(([^)]+)\)", document.read_text()):
            if "://" in target or target.startswith("#"):
                continue
            path = (document.parent / target.split("#", 1)[0]).resolve()
            assert path.is_relative_to(plugin), target
            assert path.is_file(), target
