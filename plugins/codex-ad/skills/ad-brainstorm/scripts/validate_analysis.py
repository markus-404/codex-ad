#!/usr/bin/env python3
"""Validate a product image analysis file against the vision schema.

Structural rules are hard failures. Richness is scored 0-100 and gated by
--min-score. Exits 0 only when the file is both structurally valid and rich
enough to ground 100 concepts.
"""
import argparse
import json
import re
import sys
from pathlib import Path


SHOT_TYPES = {
    "hero", "lifestyle", "detail", "macro", "packaging",
    "in-use", "scale", "comparison", "ingredient", "other",
}
PACKAGING_STYLES = {
    "matte", "glossy", "minimal", "maximalist",
    "retro", "editorial", "clinical", "playful",
}
PREMIUM_PLAYFUL = {"premium", "playful", "clinical", "editorial", "utilitarian"}

IMAGE_TEXT_FIELDS = [
    "subject", "form_factor", "materials_finish", "label_and_typography",
    "lighting", "camera_angle", "backdrop_surface", "humans", "mood",
]
ROLLUP_TEXT_FIELDS = [
    "form_factor", "brand_aesthetic_read", "who_is_in_the_photos",
    "settings_shown", "ugc_opportunity",
]

MIN_WORDS = {
    "subject": 4,
    "form_factor": 4,
    "materials_finish": 3,
    "label_and_typography": 3,
    "lighting": 3,
    "camera_angle": 2,
    "backdrop_surface": 3,
    "humans": 2,
    "mood": 2,
    "brand_aesthetic_read": 8,
    "who_is_in_the_photos": 3,
    "settings_shown": 6,
    "ugc_opportunity": 10,
}

PLACEHOLDER = re.compile(
    r"\b(todo|tbd|n/?a|lorem ipsum|placeholder|fill in|insert here|"
    r"your \w+ here|describe the|example \w+|xxx+)\b",
    re.IGNORECASE,
)
HEX = re.compile(r"^#[0-9a-fA-F]{6}$")
HUMAN_GAP = re.compile(
    r"\b(human|humans|people|person|face|faces|hand|hands|skin|model|models|ugc|creator)\b",
    re.IGNORECASE,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate product image analysis JSON against the vision schema."
    )
    parser.add_argument("--analysis", required=True)
    parser.add_argument("--min-score", type=int, default=75)
    return parser.parse_args()


def words(value: str) -> int:
    return len([w for w in re.split(r"\s+", value.strip()) if w])


def check_text(value, label: str, errors: list) -> str:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label}: missing or empty")
        return ""
    if PLACEHOLDER.search(value):
        errors.append(f"{label}: placeholder text ({value.strip()[:40]!r})")
        return value
    key = label.split(".")[-1]
    minimum = MIN_WORDS.get(key)
    if minimum and words(value) < minimum:
        errors.append(f"{label}: needs >= {minimum} words, got {words(value)}")
    return value


def check_hexes(value, label: str, minimum: int, errors: list) -> list:
    if not isinstance(value, list):
        errors.append(f"{label}: must be a list")
        return []
    valid = [h for h in value if isinstance(h, str) and HEX.match(h.strip())]
    bad = [h for h in value if not (isinstance(h, str) and HEX.match(h.strip()))]
    for h in bad:
        errors.append(f"{label}: {h!r} is not a #rrggbb hex")
    if len(valid) < minimum:
        errors.append(f"{label}: needs >= {minimum} valid hex values, got {len(valid)}")
    return valid


def validate_images(images, errors: list, warnings: list) -> list:
    if not isinstance(images, list) or not images:
        errors.append("images: must be a non-empty list")
        return []
    if len(images) > 5:
        errors.append(f"images: at most 5 entries, got {len(images)}")
    if len(images) < 3:
        warnings.append(
            f"images: only {len(images)} analyzed; 3+ makes the gap analysis reliable"
        )

    seen_index = set()
    for position, image in enumerate(images):
        label = f"images[{position}]"
        if not isinstance(image, dict):
            errors.append(f"{label}: must be an object")
            continue

        index = image.get("index")
        if not isinstance(index, int) or index < 1:
            errors.append(f"{label}.index: must be a positive integer")
        elif index in seen_index:
            errors.append(f"{label}.index: duplicate index {index}")
        else:
            seen_index.add(index)

        shot = image.get("shot_type")
        if not isinstance(shot, str) or shot.strip().lower() not in SHOT_TYPES:
            errors.append(
                f"{label}.shot_type: must be one of {sorted(SHOT_TYPES)}, got {shot!r}"
            )

        for field in IMAGE_TEXT_FIELDS:
            check_text(image.get(field), f"{label}.{field}", errors)

        check_hexes(image.get("color_hexes"), f"{label}.color_hexes", 2, errors)

        props = image.get("props")
        if not isinstance(props, list):
            errors.append(f"{label}.props: must be a list (use [] when there are none)")

    triples = {
        (
            str(i.get("shot_type", "")).strip().lower(),
            str(i.get("camera_angle", "")).strip().lower(),
            str(i.get("lighting", "")).strip().lower(),
        )
        for i in images
        if isinstance(i, dict)
    }
    if len(images) > 1 and len(triples) == 1:
        errors.append(
            "images: every entry has an identical (shot_type, camera_angle, lighting) "
            "read - the photos were not analyzed individually"
        )
    return images


def validate_rollup(rollup, errors: list, warnings: list) -> dict:
    if not isinstance(rollup, dict):
        errors.append("rollup: must be an object")
        return {}

    for field in ROLLUP_TEXT_FIELDS:
        check_text(rollup.get(field), f"rollup.{field}", errors)

    check_hexes(rollup.get("color_palette"), "rollup.color_palette", 3, errors)

    style = rollup.get("packaging_style")
    if not isinstance(style, str) or style.strip().lower() not in PACKAGING_STYLES:
        errors.append(
            f"rollup.packaging_style: must be one of {sorted(PACKAGING_STYLES)}, got {style!r}"
        )

    tone = rollup.get("premium_or_playful")
    if not isinstance(tone, str) or tone.strip().lower() not in PREMIUM_PLAYFUL:
        errors.append(
            f"rollup.premium_or_playful: must be one of {sorted(PREMIUM_PLAYFUL)}, got {tone!r}"
        )

    missing = rollup.get("whats_missing")
    if not isinstance(missing, list) or not 4 <= len(missing) <= 6:
        errors.append(
            f"rollup.whats_missing: needs 4-6 items, got "
            f"{len(missing) if isinstance(missing, list) else 'non-list'}"
        )
    else:
        for i, item in enumerate(missing):
            if not isinstance(item, str) or words(item) < 3:
                errors.append(f"rollup.whats_missing[{i}]: needs >= 3 words")
            elif PLACEHOLDER.search(item):
                errors.append(f"rollup.whats_missing[{i}]: placeholder text")

    styles = rollup.get("suggested_visual_styles")
    if not isinstance(styles, list) or len(styles) != 5:
        errors.append(
            f"rollup.suggested_visual_styles: needs exactly 5 items, got "
            f"{len(styles) if isinstance(styles, list) else 'non-list'}"
        )
    else:
        for i, item in enumerate(styles):
            if not isinstance(item, str) or words(item) < 3:
                errors.append(f"rollup.suggested_visual_styles[{i}]: needs >= 3 words")
            elif PLACEHOLDER.search(item):
                errors.append(f"rollup.suggested_visual_styles[{i}]: placeholder text")

    who = str(rollup.get("who_is_in_the_photos", ""))
    says_no_humans = re.search(r"\b(no humans?|none|nobody|no people|no person)\b", who, re.IGNORECASE)
    if says_no_humans:
        gap_text = " ".join(
            [str(rollup.get("ugc_opportunity", ""))]
            + [str(x) for x in (missing if isinstance(missing, list) else [])]
        )
        if not HUMAN_GAP.search(gap_text):
            errors.append(
                "rollup: photoset shows no humans but neither whats_missing nor "
                "ugc_opportunity flags the human/UGC gap - the gap analysis was skipped"
            )
    return rollup


def score(images: list, rollup: dict) -> dict:
    usable = [i for i in images if isinstance(i, dict)]
    if not usable or not rollup:
        return {"overall": 0, "components": {}}

    prose_counts = []
    for image in usable:
        for field in IMAGE_TEXT_FIELDS:
            value = image.get(field)
            if isinstance(value, str):
                prose_counts.append(words(value))
    for field in ROLLUP_TEXT_FIELDS:
        value = rollup.get(field)
        if isinstance(value, str):
            prose_counts.append(words(value))
    mean_words = sum(prose_counts) / len(prose_counts) if prose_counts else 0

    triples = {
        (
            str(i.get("shot_type", "")).lower(),
            str(i.get("camera_angle", "")).lower(),
            str(i.get("lighting", "")).lower(),
        )
        for i in usable
    }
    distinctness = len(triples) / len(usable)

    hexes = set()
    for image in usable:
        for h in image.get("color_hexes", []) or []:
            if isinstance(h, str) and HEX.match(h.strip()):
                hexes.add(h.strip().lower())
    for h in rollup.get("color_palette", []) or []:
        if isinstance(h, str) and HEX.match(h.strip()):
            hexes.add(h.strip().lower())

    missing = [x for x in (rollup.get("whats_missing") or []) if isinstance(x, str)]
    styles = [x for x in (rollup.get("suggested_visual_styles") or []) if isinstance(x, str)]
    gap_words = sum(words(x) for x in missing) / len(missing) if missing else 0
    style_words = sum(words(x) for x in styles) / len(styles) if styles else 0

    components = {
        "detail_depth": min(100, round(mean_words / 8 * 100)),
        "image_coverage": min(100, round(len(usable) / 4 * 100)),
        "per_shot_distinctness": round(distinctness * 100),
        "palette_specificity": min(100, round(len(hexes) / 6 * 100)),
        "gap_specificity": min(100, round(gap_words / 7 * 100)),
        "style_actionability": min(100, round(style_words / 7 * 100)),
    }
    overall = round(sum(components.values()) / len(components))
    return {"overall": overall, "components": components}


def validate(path: str, min_score: int) -> dict:
    analysis_path = Path(path)
    if not analysis_path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    data = json.loads(analysis_path.read_text())

    errors: list = []
    warnings: list = []
    images = validate_images(data.get("images"), errors, warnings)
    rollup = validate_rollup(data.get("rollup"), errors, warnings)
    scored = score(images if isinstance(images, list) else [], rollup)

    if not errors and scored["overall"] < min_score:
        errors.append(
            f"score {scored['overall']} is below --min-score {min_score}; "
            "add specificity to the weakest components before generating concepts"
        )

    return {
        "passed": not errors,
        "score": scored["overall"],
        "min_score": min_score,
        "components": scored["components"],
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    args = parse_args()
    try:
        result = validate(args.analysis, args.min_score)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
