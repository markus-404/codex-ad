#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

import yaml


STRATEGIES = [
    {
        "name": "Create alternate versions",
        "rationale": "Keep the proven product and offer while varying the focal point and supporting scene.",
    },
    {
        "name": "Iterate messaging",
        "rationale": "Keep the visual system close to the winner while testing different copy angles.",
    },
    {
        "name": "Add floating callouts or pop-ups",
        "rationale": "Use overlay elements to direct attention toward benefits, proof, and the offer.",
    },
]

IDEA_SUFFIXES = [
    "Hero Product Counter",
    "Offer First Layout",
    "Persona Scene Variant",
    "Proof And Callout Variant",
]


def load_yaml(path: str) -> dict:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    with file_path.open() as file:
        data = yaml.safe_load(file)
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path}")
    return data


def build_idea(strategy_name: str, suffix: str, product: dict, persona: dict, scenario: dict) -> dict:
    product_name = product["name"]
    persona_name = persona["name"]
    scene = scenario["scene"]
    offer_message = product.get("unique_selling_points", ["Clear product benefit"])[0]
    return {
        "name": f"{product_name} {suffix}",
        "scene": f"{scene} Adapt the composition for the {strategy_name.lower()} strategy.",
        "persona_target": persona_name,
        "rationale": f"This concept uses {suffix.lower()} to make {product_name} feel relevant to {persona_name}.",
        "key_message": offer_message,
        "emotion": scenario.get("emotional_state", "confident"),
        "theme": strategy_name,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a structured 3x4 static ad iteration ladder.")
    parser.add_argument("--brand", required=True)
    parser.add_argument("--product", required=True)
    parser.add_argument("--persona", required=True)
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--original-ad-summary", required=True)
    parser.add_argument("--performance-notes", required=True)
    parser.add_argument("--out", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        product = load_yaml(args.product)
        persona = load_yaml(args.persona)
        scenario = load_yaml(args.scenario)
        load_yaml(args.brand)
        strategies = []
        for strategy in STRATEGIES:
            strategies.append({
                "name": strategy["name"],
                "rationale": strategy["rationale"],
                "ad_ideas": [
                    build_idea(strategy["name"], suffix, product, persona, scenario)
                    for suffix in IDEA_SUFFIXES
                ],
            })
        output = {
            "original_ad": {
                "summary": args.original_ad_summary,
                "performance_notes": args.performance_notes,
            },
            "strategies": strategies,
        }
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
        return 0
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
