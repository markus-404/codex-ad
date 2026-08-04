#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path

import yaml


FIELD_ALIASES = {
    "brand": "brand",
    "website": "website",
    "product": "product",
    "product url": "product_url",
    "product category": "product_category",
    "product description": "product_description",
    "audience": "audience",
    "persona": "persona",
    "scenario": "scenario",
    "scene": "scene",
    "problem": "problem",
    "desired outcome": "desired_outcome",
    "offer": "offer",
    "platform": "platform",
    "objective": "objective",
    "tone": "tone",
    "assets": "assets",
    "must include": "must_include",
    "must avoid": "must_avoid",
}

REQUIRED_FIELDS = [
    "brand",
    "product",
    "audience",
    "persona",
    "scenario",
    "scene",
    "offer",
    "platform",
    "objective",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scaffold ad-maker campaign YAML from a marketer brief.")
    parser.add_argument("--brief", required=True)
    parser.add_argument("--out-dir", required=True)
    return parser.parse_args()


def normalize_heading(line: str) -> str:
    return line.strip().rstrip(":").lower()


def parse_brief(text: str) -> dict:
    fields = {}
    current = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        key = FIELD_ALIASES.get(normalize_heading(line))
        if key:
            current = key
            fields.setdefault(current, [])
            continue
        if current and line.strip():
            fields[current].append(line.strip())
    parsed = {key: "\n".join(value).strip() for key, value in fields.items()}
    missing = [field for field in REQUIRED_FIELDS if not parsed.get(field)]
    if missing:
        raise ValueError("Missing required brief fields: " + ", ".join(missing))
    return parsed


def list_from_text(value: str) -> list:
    items = []
    for line in value.splitlines():
        cleaned = re.sub(r"^[-*]\s*", "", line).strip()
        if cleaned:
            items.append(cleaned)
    return items


def parse_assets(value: str) -> dict:
    assets = {}
    for item in list_from_text(value):
        if ":" in item:
            name, path = item.split(":", 1)
            assets[name.strip().lower()] = path.strip()
    return assets


def split_problem(value: str) -> list:
    parts = []
    for chunk in re.split(r";|\n", value):
        cleaned = chunk.strip()
        if cleaned:
            parts.append(cleaned)
    return parts or ["unclear barrier"]


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=False))


def build_files(fields: dict) -> dict:
    assets = parse_assets(fields.get("assets", ""))
    must_include = list_from_text(fields.get("must_include", ""))
    must_avoid = list_from_text(fields.get("must_avoid", ""))
    product_category = fields.get("product_category", "Product")
    product_description = fields.get("product_description", fields["product"])
    tone = fields.get("tone", "Clear, useful, and brand-safe.")

    brand = {
        "name": fields["brand"],
        "website": fields.get("website", "https://example.com"),
        "vertical": [product_category],
        "description": fields["audience"],
        "unique_value_propositions": must_include or [fields["offer"]],
        "target_audience": fields["audience"],
        "category": product_category,
        "category_needs": split_problem(fields.get("problem", fields["offer"])),
        "notes": f"Scaffolded from campaign brief for {fields['platform']}.",
        "guidelines": {
            "logos": [{
                "path": assets.get("logo", "./assets/logo.png"),
                "label": f"{fields['brand']} logo",
                "default": True,
            }],
            "colors": ["#337AB7", "#FFFFFF", "#DAB86D"],
            "fonts": {
                "headline": {"family": "Brand headline font", "weight": "regular"},
                "body": {"family": "Brand body font", "weight": "regular"},
            },
            "tone": tone,
            "preferred_words": must_include or ["clear", "simple"],
            "avoid_words": must_avoid or ["generic"],
        },
    }
    product = {
        "name": fields["product"],
        "url": fields.get("product_url", "https://example.com/product"),
        "categories": [product_category],
        "description": product_description,
        "unique_selling_points": must_include or [fields["offer"]],
        "images": [{
            "path": assets.get("product", "./assets/product.png"),
            "label": f"{fields['product']} product image",
        }],
        "related_scenarios": [fields["scenario"]],
        "related_personas": [fields["persona"]],
        "awareness_level": "L4 Product/brand aware",
        "market_sophistication": "L4",
    }
    persona = {
        "name": fields["persona"],
        "summary": fields["audience"],
        "core_motivations": [fields.get("desired_outcome", fields["offer"])],
        "barriers_objections": split_problem(fields.get("problem", "")),
        "what_convinces": must_include or [fields["offer"]],
        "preferred_channels": [fields["platform"]],
    }
    scenario = {
        "name": fields["scenario"],
        "scene": fields["scene"],
        "trigger": fields.get("problem", fields["offer"]),
        "pain_points": split_problem(fields.get("problem", "")),
        "desired_outcome": fields.get("desired_outcome", fields["offer"]),
        "emotional_state": "Interested and ready to act.",
        "current_alternatives": ["doing nothing", "competitor product"],
        "barrier": split_problem(fields.get("problem", ""))[0],
    }
    campaign = {
        "platform": fields["platform"],
        "objective": fields["objective"],
        "offer": fields["offer"],
        "headline": fields.get("headline", fields["offer"]),
        "subline": product_description,
    }
    return {
        "brand.yaml": brand,
        "product.yaml": product,
        "persona.yaml": persona,
        "scenario.yaml": scenario,
        "campaign.md": campaign,
    }


def main() -> int:
    args = parse_args()
    try:
        brief_path = Path(args.brief)
        if not brief_path.exists():
            raise FileNotFoundError(f"Missing file: {args.brief}")
        fields = parse_brief(brief_path.read_text())
        files = build_files(fields)
        out_dir = Path(args.out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        for name, data in files.items():
            if name.endswith(".yaml"):
                write_yaml(out_dir / name, data)
            else:
                lines = [f"# Campaign\n"]
                for key, value in data.items():
                    lines.append(f"{key}: {value}")
                (out_dir / name).write_text("\n".join(lines) + "\n")
        return 0
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
