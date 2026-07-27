#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

import yaml


RATIO_TO_SIZE = {
    "1:1": "1024x1024",
    "4:5": "1024x1280",
    "9:16": "1152x2048",
}
PRESET_PATH = Path(__file__).resolve().parents[1] / "references/platform-presets.yaml"

MODES = {"brief", "clone", "iterate"}
REFINE_MODES = {
    "reuse_prompt",
    "reuse_ad_brief",
    "style",
    "layout",
    "scenario",
    "persona",
    "subtle",
    "strong",
    "text_edit",
    "inpaint",
}

NEGATIVE_PROMPT_LINES = [
    "- Do not use logos other than uploaded #0; do not restyle or redraw logo or wordmark.",
    "- No garbled typography, distorted logo, or extraneous watermarks.",
    "- No unrelated or competing product visuals.",
    "- No invented wordmark next to the logo.",
    "- Do not alter product shape, label geometry, cap shape, package proportions, or visible product materials.",
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


def load_platform_presets() -> dict:
    data = load_yaml(str(PRESET_PATH))
    return data


def apply_platform_preset(args: argparse.Namespace) -> None:
    args.platform_preset_data = {}
    if not args.platform_preset:
        return
    presets = load_platform_presets()
    preset = presets.get(args.platform_preset)
    if not preset:
        raise ValueError(f"Unsupported platform preset: {args.platform_preset}")
    args.platform_preset_data = preset
    if not args.ratio:
        args.ratio = preset.get("ratio")
    if not args.objective:
        args.objective = preset.get("objective")


def require_args(args: argparse.Namespace, names: list) -> None:
    missing = [name for name in names if getattr(args, name) in (None, "")]
    if missing:
        raise ValueError("Missing required arguments: " + ", ".join(f"--{name.replace('_', '-')}" for name in missing))


def font_label(font: dict) -> str:
    family = font.get("family", "brand font")
    weight = font.get("weight", "regular")
    return f"{family} {weight}"


def resolve_ref_path(raw_path: str, base_dir: Path) -> str:
    if not raw_path:
        return ""
    candidate = Path(raw_path)
    if not candidate.is_absolute():
        candidate = base_dir / candidate
    return str(candidate.resolve())


def collect_image_refs(brand: dict, product: dict, brand_dir: Path, product_dir: Path) -> list:
    refs = []
    logos = brand.get("guidelines", {}).get("logos", [])
    default_logo = next((logo for logo in logos if logo.get("default")), logos[0] if logos else None)
    if default_logo:
        refs.append({
            "index": len(refs),
            "role": "logo",
            "path": resolve_ref_path(default_logo.get("path", ""), brand_dir),
            "label": default_logo.get("label", f"{brand.get('name', 'Brand')} logo"),
        })
    for image in product.get("images", []):
        refs.append({
            "index": len(refs),
            "role": "product",
            "path": resolve_ref_path(image.get("path", ""), product_dir),
            "label": image.get("label", f"{product.get('name', 'Product')} product image"),
        })
    return refs


def build_prompt(brand: dict, product: dict, persona: dict, scenario: dict, args: argparse.Namespace) -> dict:
    if args.ratio not in RATIO_TO_SIZE:
        raise ValueError(f"Unsupported ratio: {args.ratio}")
    if args.mode not in MODES:
        raise ValueError(f"Unsupported mode: {args.mode}")
    if args.variant_count < 1:
        raise ValueError("--variant-count must be at least 1.")

    brand_name = brand["name"]
    product_name = product["name"]
    persona_name = persona["name"]
    scenario_name = scenario["name"]
    scene = scenario["scene"]
    colors = ", ".join(brand.get("guidelines", {}).get("colors", []))
    headline_font = font_label(brand.get("guidelines", {}).get("fonts", {}).get("headline", {}))
    body_font = font_label(brand.get("guidelines", {}).get("fonts", {}).get("body", {}))
    preset = getattr(args, "platform_preset_data", {}) or {}

    visual = args.visual or (
        f"{scene} Feature {product_name} for {persona_name}, with a small value callout reading \"{args.offer}\"."
    )
    if args.layout:
        layout = args.layout
    elif preset.get("layout_guidance"):
        layout = (
            f"{preset['layout_guidance']} Use uploaded product #1 as the product reference; "
            f"place headline \"{args.headline}\" and offer \"{args.offer}\" in the primary reading path."
        )
    else:
        layout = (
            f"Place uploaded product #1 as the central visual occupying at least 12% of the canvas; "
            f"place headline \"{args.headline}\" at top center and offer \"{args.offer}\" in a rounded callout near the product."
        )
    if preset and preset.get("creative_style"):
        visual = f"{visual} Creative style: {preset['creative_style']}"

    prompt_lines = [
        f"- Visual: {visual}",
        f"- Color: Use {colors} as the brand palette, with the first color as the dominant accent, white or open space for clarity, and premium highlights where useful.",
        f"- Layout: {layout}",
        f"- Text: Headline \"{args.headline}\"; subline \"{args.subline}\"; offer \"{args.offer}\".",
        f"- Fonts: Use {headline_font} for the headline and {body_font} for subline, callouts, and body copy.",
        "- Logo: Place uploaded logo #0 at top left; preserve the uploaded wordmark exactly and do not redraw, restyle, re-letter, or substitute typography.",
    ]

    return {
        "prompt": "\n".join(prompt_lines),
        "negative_prompt": "\n".join(NEGATIVE_PROMPT_LINES),
        "image_refs": collect_image_refs(
            brand,
            product,
            Path(args.brand).resolve().parent,
            Path(args.product).resolve().parent,
        ),
        "metadata": {
            "mode": args.mode,
            "objective": args.objective,
            "ratio": args.ratio,
            "size": RATIO_TO_SIZE[args.ratio],
            "platform_preset": args.platform_preset or "",
            "variant_count": args.variant_count,
            "brand": brand_name,
            "product": product_name,
            "persona": persona_name,
            "scenario": scenario_name,
            "lineage": {
                "source": "natural_language_request" if args.mode == "brief" else args.mode,
                "refine_mode": "none",
                "source_prompt_json": "",
            },
        },
    }


def refine_prompt(args: argparse.Namespace) -> dict:
    if args.refine_mode not in REFINE_MODES:
        raise ValueError(f"Unsupported refine mode: {args.refine_mode}")
    source_path = Path(args.source_prompt_json)
    if not source_path.exists():
        raise FileNotFoundError(f"Missing file: {args.source_prompt_json}")
    data = json.loads(source_path.read_text())
    data["prompt"] = data["prompt"] + f"\nRefinement instruction: {args.edit_instruction}"
    metadata = data.setdefault("metadata", {})
    lineage = metadata.setdefault("lineage", {})
    lineage["refine_mode"] = args.refine_mode
    lineage["source_prompt_json"] = args.source_prompt_json
    return data


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile structured ad image prompts.")
    parser.add_argument("--brand")
    parser.add_argument("--product")
    parser.add_argument("--persona")
    parser.add_argument("--scenario")
    parser.add_argument("--mode", choices=sorted(MODES))
    parser.add_argument("--objective")
    parser.add_argument("--ratio")
    parser.add_argument("--platform-preset")
    parser.add_argument("--variant-count", type=int)
    parser.add_argument("--headline")
    parser.add_argument("--subline")
    parser.add_argument("--offer")
    parser.add_argument("--visual")
    parser.add_argument("--layout")
    parser.add_argument("--source-prompt-json")
    parser.add_argument("--refine-mode", choices=sorted(REFINE_MODES))
    parser.add_argument("--edit-instruction")
    parser.add_argument("--out", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.source_prompt_json:
            require_args(args, ["source_prompt_json", "refine_mode", "edit_instruction", "out"])
            output = refine_prompt(args)
        else:
            apply_platform_preset(args)
            require_args(args, ["brand", "product", "persona", "scenario", "mode", "objective", "ratio", "variant_count", "headline", "subline", "offer", "out"])
            brand = load_yaml(args.brand)
            product = load_yaml(args.product)
            persona = load_yaml(args.persona)
            scenario = load_yaml(args.scenario)
            output = build_prompt(brand, product, persona, scenario, args)
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
        return 0
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
