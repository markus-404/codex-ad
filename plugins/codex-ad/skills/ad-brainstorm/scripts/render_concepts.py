#!/usr/bin/env python3
"""Render validated concepts JSON into marketer-facing markdown.

concepts.json is the source of truth; concepts.md is generated. Grouped by
format archetype so the doc can be scanned by row.
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render concepts JSON into grouped markdown."
    )
    parser.add_argument("--concepts", required=True)
    parser.add_argument("--out", required=True)
    return parser.parse_args()


def render(data: dict) -> str:
    product = data.get("product", {})
    grid = data.get("grid", {})
    formats = grid.get("formats", [])
    angles = grid.get("angles", [])
    concepts = data.get("concepts", [])

    by_format = defaultdict(list)
    for concept in concepts:
        by_format[concept.get("format_index")].append(concept)

    title = product.get("title") or "Untitled product"
    lines = ["# Ad Concepts - {0}".format(title), ""]

    meta = []
    if product.get("brand"):
        meta.append("**Brand:** {0}".format(product["brand"]))
    if product.get("price"):
        meta.append("**Price:** {0}".format(product["price"]))
    if product.get("url"):
        meta.append("**Source:** {0}".format(product["url"]))
    if meta:
        lines.extend([" | ".join(meta), ""])

    lines.extend([
        "**Grid:** {0} formats x {1} angles = {2} concepts".format(
            len(formats), len(angles), len(concepts)
        ),
        "",
        "---",
        "",
    ])

    for position, format_name in enumerate(formats):
        format_index = position + 1
        rows = sorted(by_format.get(format_index, []), key=lambda c: c.get("angle_index", 0))
        lines.extend(["## F{0} - {1}".format(format_index, format_name), ""])
        if not rows:
            lines.extend(["_No concepts generated for this format._", ""])
            continue
        for concept in rows:
            lines.extend([
                "### {0} - {1} x {2}".format(
                    concept.get("id", "?"),
                    format_name,
                    concept.get("angle", "?"),
                ),
                "",
                "**Hook:** {0}".format(concept.get("hook", "")),
                "",
            ])
            summary = concept.get("summary", [])
            for position, line in enumerate(summary):
                # Trailing double space keeps the two beats on separate rendered lines.
                lines.append(line + "  " if position < len(summary) - 1 else line)
            lines.extend([
                "",
                "**Visual:** {0}".format(concept.get("visual_style", "")),
                "",
                "**Grounded in:** {0}".format(
                    ", ".join("`{0}`".format(p) for p in concept.get("visual_grounding", []))
                ),
                "",
                "**Platform:** {0}".format(concept.get("platform", "")),
                "",
            ])
        lines.append("---")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    try:
        concepts_path = Path(args.concepts)
        if not concepts_path.exists():
            raise FileNotFoundError("Missing file: {0}".format(args.concepts))
        data = json.loads(concepts_path.read_text())
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(render(data))
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print("wrote {0}".format(args.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
