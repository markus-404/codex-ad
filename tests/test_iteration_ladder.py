import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins/ad-maker/skills/ad-maker/scripts/create_iteration_ladder.py"
EXAMPLES = ROOT / "plugins/ad-maker/skills/ad-maker/references/examples"


def test_iteration_ladder_has_three_strategies_and_twelve_ideas(tmp_path):
    output = tmp_path / "ladder.json"
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
        "--original-ad-summary",
        "Product bottle on a kitchen counter with discount badge",
        "--performance-notes",
        "ROAS 4.2, CTR 2.1%, strong offer response",
        "--out",
        str(output),
    ]
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    data = json.loads(output.read_text())
    assert len(data["strategies"]) == 3
    assert sum(len(strategy["ad_ideas"]) for strategy in data["strategies"]) == 12
    for strategy in data["strategies"]:
        assert len(strategy["ad_ideas"]) == 4
        assert strategy["name"]
        assert strategy["rationale"]
        for idea in strategy["ad_ideas"]:
            assert idea["name"]
            assert idea["scene"]
            assert idea["persona_target"] == "Busy Home Cook"
            assert idea["rationale"]
