import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/codex-ad"
SKILL = PLUGIN / "skills/ad-brainstorm"


def test_skill_is_self_contained():
    """Every file the skill references must live inside the skill directory."""
    for name in ["SKILL.md", "references/vision-schema.md", "references/concept-schema.md",
                 "references/grid.md", "references/scrape-routes.md",
                 "scripts/validate_analysis.py", "scripts/validate_concepts.py",
                 "scripts/render_concepts.py"]:
        assert (SKILL / name).exists(), "missing {0}".format(name)


def test_skill_md_never_uses_repo_relative_script_paths():
    """Installed plugins do not sit under the user's cwd - repo paths would break."""
    text = (SKILL / "SKILL.md").read_text()
    assert "python3 plugins/" not in text
    assert "plugins/codex-ad/skills" not in text
    for match in re.findall(r"python3 \"?([^\s\"]+)", text):
        assert match.startswith("$SKILL_DIR/"), (
            "script invocation {0!r} must be resolved from $SKILL_DIR".format(match)
        )


def test_skill_md_documents_skill_dir():
    text = (SKILL / "SKILL.md").read_text()
    assert "$SKILL_DIR" in text
    assert "CLAUDE_PLUGIN_ROOT" in text


def test_scripts_use_only_stdlib():
    """Sandboxed hosts (claude.ai) have no third-party packages and no network."""
    banned = {"yaml", "requests", "openai", "PIL", "httpx", "urllib3"}
    for script in (SKILL / "scripts").glob("*.py"):
        source = script.read_text()
        for module in banned:
            assert not re.search(r"^\s*(import|from)\s+{0}\b".format(module), source, re.M), (
                "{0} imports {1}".format(script.name, module)
            )


def test_scripts_make_no_network_calls():
    for script in (SKILL / "scripts").glob("*.py"):
        source = script.read_text()
        for token in ["urlopen", "http://", "https://generativelanguage", "socket"]:
            assert token not in source, "{0} contains {1}".format(script.name, token)


def test_no_api_key_dependency_remains():
    for path in list(SKILL.rglob("*.md")) + list(SKILL.rglob("*.py")):
        text = path.read_text()
        assert "api-keys.json" not in text, "{0} still references an API key file".format(path)
        assert "gemini_api_key" not in text, "{0} still references a Gemini key".format(path)


def test_codex_and_claude_manifests_agree():
    codex = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text())
    claude = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text())
    assert codex["name"] == claude["name"] == "codex-ad"
    assert codex["version"] == claude["version"]


def test_both_skills_ship_in_the_one_plugin():
    """One install must deliver both skills - they are not separate plugins."""
    skills = {p.name for p in (PLUGIN / "skills").iterdir() if p.is_dir()}
    assert skills == {"ad-brainstorm", "ad-maker"}
    for skill in skills:
        assert (PLUGIN / "skills" / skill / "SKILL.md").exists()


def test_skill_frontmatter_name_matches_directory():
    for skill in (PLUGIN / "skills").iterdir():
        if not skill.is_dir():
            continue
        header = (skill / "SKILL.md").read_text().split("---")[1]
        assert re.search(r"^name:\s*{0}\s*$".format(skill.name), header, re.M), (
            "{0}/SKILL.md frontmatter name does not match its directory".format(skill.name)
        )


def test_marketplace_lists_every_plugin():
    marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    listed = {p["name"] for p in marketplace["plugins"]}
    on_disk = {p.name for p in (ROOT / "plugins").iterdir() if p.is_dir()}
    assert listed == on_disk, "marketplace.json is out of sync with plugins/"
    for entry in marketplace["plugins"]:
        source = ROOT / entry["source"]
        assert (source / ".claude-plugin/plugin.json").exists(), (
            "{0} has no Claude plugin manifest".format(entry["name"])
        )


def test_codex_marketplace_lists_every_plugin():
    """Codex reads .agents/plugins/marketplace.json, not the Claude one."""
    marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
    listed = {p["name"] for p in marketplace["plugins"]}
    on_disk = {p.name for p in (ROOT / "plugins").iterdir() if p.is_dir()}
    assert listed == on_disk, ".agents/plugins/marketplace.json is out of sync with plugins/"
    for entry in marketplace["plugins"]:
        source = ROOT / entry["source"]["path"]
        assert (source / ".codex-plugin/plugin.json").exists(), (
            "{0} source path does not resolve to a Codex plugin".format(entry["name"])
        )


def test_both_marketplaces_agree():
    claude = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    codex = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
    assert claude["name"] == codex["name"]
    assert {p["name"] for p in claude["plugins"]} == {p["name"] for p in codex["plugins"]}


def test_old_gemini_skill_is_gone():
    assert not (ROOT / "one-to-100/.claude").exists()
