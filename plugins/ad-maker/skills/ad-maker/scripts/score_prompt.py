#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path

import yaml


PRESET_PATH = Path(__file__).resolve().parents[1] / "references/platform-presets.yaml"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score compiled ad-maker prompt JSON with a deterministic rubric.")
    parser.add_argument("--prompt-json", required=True)
    return parser.parse_args()


def load_prompt(path: str) -> dict:
    prompt_path = Path(path)
    if not prompt_path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return json.loads(prompt_path.read_text())


def load_presets() -> dict:
    return yaml.safe_load(PRESET_PATH.read_text())


def quoted_text_count(prompt: str) -> int:
    return len(re.findall(r'"[^"]+"', prompt))


def contains_any(text: str, needles: list) -> bool:
    lower = text.lower()
    return any(needle in lower for needle in needles)


def has_role(prompt_data: dict, role: str) -> bool:
    return any(ref.get("role") == role for ref in prompt_data.get("image_refs", []))


def score_prompt(prompt_data: dict) -> dict:
    prompt = prompt_data.get("prompt", "")
    negative = prompt_data.get("negative_prompt", "")
    metadata = prompt_data.get("metadata", {})
    preset_name = metadata.get("platform_preset", "")
    preset = load_presets().get(preset_name, {}) if preset_name else {}
    text = f"{prompt}\n{negative}"
    lower = text.lower()
    risks = []
    recommendations = []

    scores = {
        "hook_clarity": 10 if contains_any(prompt, ["hook", "foreground", "plating", "scene", "handheld"]) else 6,
        "product_prominence": 10 if has_role(prompt_data, "product") and contains_any(prompt, ["product", "foreground", "at least 18%", "22%"]) else 5,
        "offer_clarity": 10 if contains_any(prompt, ["offer", "save", "trial", "discount", "cta"]) and quoted_text_count(prompt) >= 2 else 5,
        "audience_fit": 9 if contains_any(prompt, ["busy", "persona", "audience", "customer", "cook", "team"]) else 6,
        "brand_consistency": 10 if has_role(prompt_data, "logo") and contains_any(prompt, ["fonts", "logo", "#"]) else 6,
        "platform_fit": 10 if preset and metadata.get("ratio") == preset.get("ratio") else (7 if metadata.get("ratio") else 4),
        "text_render_risk": 9 if quoted_text_count(prompt) <= 6 and "- Text:" in prompt and "- Layout:" in prompt else 5,
        "product_fidelity_risk": 10 if has_role(prompt_data, "product") and contains_any(negative, ["do not alter product", "product shape"]) else 5,
        "novelty": 9 if len(prompt) > 300 and contains_any(prompt, ["scene", "foreground", "lighting", "mood", "safe zone"]) else 6,
    }

    if not has_role(prompt_data, "product"):
        risks.append("Missing product reference image.")
        recommendations.append("Add a product image reference and state where it appears in the layout.")
    if not has_role(prompt_data, "logo"):
        risks.append("Missing logo reference image.")
        recommendations.append("Add a logo reference and preserve uploaded logo #0.")
    if scores["offer_clarity"] < 8:
        risks.append("Offer or CTA is not clear enough.")
        recommendations.append("Quote the offer once in Layout and once in Text.")
    if scores["platform_fit"] < 8:
        risks.append("Prompt ratio does not clearly match the platform preset.")
        recommendations.append("Use a platform preset or set the ratio expected by the channel.")
    if scores["product_fidelity_risk"] < 8:
        risks.append("Product fidelity safeguards are weak.")
        recommendations.append("Add negative prompt language that prevents product shape and label drift.")

    overall = round(sum(scores.values()) / len(scores) * 10)
    return {
        "overall_score": overall,
        "scores": scores,
        "risks": risks,
        "recommendations": recommendations,
    }


def main() -> int:
    args = parse_args()
    try:
        result = score_prompt(load_prompt(args.prompt_json))
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
