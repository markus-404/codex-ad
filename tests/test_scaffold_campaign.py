import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins/ad-maker/skills/ad-maker/scripts/scaffold_campaign.py"
BRIEF = ROOT / "examples/campaign-brief.md"


def test_scaffold_campaign_creates_marketer_yaml_files(tmp_path):
    out_dir = tmp_path / "campaign"
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--brief",
            str(BRIEF),
            "--out-dir",
            str(out_dir),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    expected = ["brand.yaml", "product.yaml", "persona.yaml", "scenario.yaml", "campaign.md"]
    for name in expected:
        assert (out_dir / name).exists(), name

    brand = yaml.safe_load((out_dir / "brand.yaml").read_text())
    product = yaml.safe_load((out_dir / "product.yaml").read_text())
    persona = yaml.safe_load((out_dir / "persona.yaml").read_text())
    scenario = yaml.safe_load((out_dir / "scenario.yaml").read_text())

    assert brand["name"] == "Sample Foods"
    assert brand["guidelines"]["logos"][0]["path"] == "./assets/logo.png"
    assert product["name"] == "Sample Bottle"
    assert product["images"][0]["path"] == "./assets/product.png"
    assert persona["name"] == "Busy Home Cook"
    assert scenario["name"] == "Weeknight dinner upgrade"
    assert "meta-feed-conversion" in (out_dir / "campaign.md").read_text()


def test_scaffold_campaign_requires_known_brief_sections(tmp_path):
    brief = tmp_path / "bad-brief.md"
    brief.write_text("# Campaign Brief\n\nBrand:\nOnly a brand\n")
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--brief",
            str(brief),
            "--out-dir",
            str(tmp_path / "campaign"),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode != 0
    assert "Missing required brief fields" in result.stderr
