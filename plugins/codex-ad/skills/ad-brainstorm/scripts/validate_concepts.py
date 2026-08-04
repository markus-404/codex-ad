#!/usr/bin/env python3
"""Validate a generated concept grid against the concept schema.

Hard-checks full grid coverage, ID/label agreement, hook uniqueness, and that
every concept's visual_grounding resolves to a real element of analysis.json.
Quality signals are scored 0-100 and gated by --min-score.
"""
import argparse
import json
import re
import sys
from pathlib import Path


PLATFORMS = {
    "Meta feed", "Meta Reels", "TikTok", "YouTube Shorts",
    "YouTube long-form", "Reddit", "LinkedIn", "Pinterest",
}
MAX_HOOK_WORDS = 15
MIN_SUMMARY_WORDS = 6
MIN_VISUAL_STYLE_WORDS = 4
NEAR_DUPLICATE_JACCARD = 0.7

PLACEHOLDER = re.compile(
    r"\b(todo|tbd|n/?a|lorem ipsum|placeholder|fill in|insert here|"
    r"your \w+ here|example hook|xxx+)\b",
    re.IGNORECASE,
)
PATH_SEGMENT = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)(\[(\d+)\])?$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate concepts JSON against the concept schema."
    )
    parser.add_argument("--concepts", required=True)
    parser.add_argument("--analysis", required=True)
    parser.add_argument("--min-score", type=int, default=75)
    return parser.parse_args()


def words(value: str) -> list:
    return [w for w in re.split(r"\s+", value.strip()) if w]


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", "", value.lower())).strip()


def resolve_path(analysis: dict, path: str):
    """Resolve 'images[0].lighting' style paths. Returns (ok, value)."""
    current = analysis
    for segment in path.split("."):
        match = PATH_SEGMENT.match(segment.strip())
        if not match:
            return False, None
        name, _, index = match.groups()
        if not isinstance(current, dict) or name not in current:
            return False, None
        current = current[name]
        if index is not None:
            if not isinstance(current, list):
                return False, None
            position = int(index)
            if position >= len(current):
                return False, None
            current = current[position]
    return True, current


def validate_grid(grid, errors: list):
    if not isinstance(grid, dict):
        errors.append("grid: must be an object")
        return [], []
    formats = grid.get("formats")
    angles = grid.get("angles")
    if not isinstance(formats, list) or not formats:
        errors.append("grid.formats: must be a non-empty list")
        formats = []
    if not isinstance(angles, list) or not angles:
        errors.append("grid.angles: must be a non-empty list")
        angles = []
    return formats, angles


def validate_concepts(concepts, formats, angles, analysis, errors: list, warnings: list):
    if not isinstance(concepts, list):
        errors.append("concepts: must be a list")
        return []

    expected_cells = {
        "F{0}-A{1}".format(f + 1, a + 1)
        for f in range(len(formats))
        for a in range(len(angles))
    }
    seen_cells: dict = {}
    seen_hooks: dict = {}
    valid: list = []

    for position, concept in enumerate(concepts):
        label = "concepts[{0}]".format(position)
        if not isinstance(concept, dict):
            errors.append("{0}: must be an object".format(label))
            continue

        cid = concept.get("id")
        fi = concept.get("format_index")
        ai = concept.get("angle_index")

        if not isinstance(fi, int) or not 1 <= fi <= len(formats):
            errors.append("{0}.format_index: out of range 1..{1}".format(label, len(formats)))
            continue
        if not isinstance(ai, int) or not 1 <= ai <= len(angles):
            errors.append("{0}.angle_index: out of range 1..{1}".format(label, len(angles)))
            continue

        expected_id = "F{0}-A{1}".format(fi, ai)
        if cid != expected_id:
            errors.append(
                "{0}.id: {1!r} does not match its cell (expected {2!r})".format(
                    label, cid, expected_id
                )
            )
            continue

        if expected_id in seen_cells:
            errors.append(
                "{0}: duplicate cell {1} (already at concepts[{2}])".format(
                    label, expected_id, seen_cells[expected_id]
                )
            )
            continue
        seen_cells[expected_id] = position

        if concept.get("format") != formats[fi - 1]:
            errors.append(
                "{0}.format: {1!r} does not match grid.formats[{2}] ({3!r})".format(
                    label, concept.get("format"), fi - 1, formats[fi - 1]
                )
            )
        if concept.get("angle") != angles[ai - 1]:
            errors.append(
                "{0}.angle: {1!r} does not match grid.angles[{2}] ({3!r})".format(
                    label, concept.get("angle"), ai - 1, angles[ai - 1]
                )
            )

        hook = concept.get("hook")
        if not isinstance(hook, str) or not hook.strip():
            errors.append("{0}.hook: missing or empty".format(label))
        elif PLACEHOLDER.search(hook):
            errors.append("{0}.hook: placeholder text".format(label))
        elif len(words(hook)) > MAX_HOOK_WORDS:
            errors.append(
                "{0}.hook: {1} words, limit is {2}".format(
                    label, len(words(hook)), MAX_HOOK_WORDS
                )
            )
        else:
            key = normalize(hook)
            if key in seen_hooks:
                errors.append(
                    "{0}.hook: duplicate of {1} ({2!r})".format(label, seen_hooks[key], hook)
                )
            else:
                seen_hooks[key] = expected_id

        summary = concept.get("summary")
        if not isinstance(summary, list) or len(summary) != 2:
            errors.append("{0}.summary: must be exactly 2 lines".format(label))
        else:
            for i, line in enumerate(summary):
                if not isinstance(line, str) or len(words(line)) < MIN_SUMMARY_WORDS:
                    errors.append(
                        "{0}.summary[{1}]: needs >= {2} words".format(
                            label, i, MIN_SUMMARY_WORDS
                        )
                    )
                elif PLACEHOLDER.search(line):
                    errors.append("{0}.summary[{1}]: placeholder text".format(label, i))

        style = concept.get("visual_style")
        if not isinstance(style, str) or len(words(style)) < MIN_VISUAL_STYLE_WORDS:
            errors.append(
                "{0}.visual_style: needs >= {1} words".format(label, MIN_VISUAL_STYLE_WORDS)
            )
        elif PLACEHOLDER.search(style):
            errors.append("{0}.visual_style: placeholder text".format(label))

        grounding = concept.get("visual_grounding")
        if not isinstance(grounding, list) or not grounding:
            errors.append(
                "{0}.visual_grounding: must be a non-empty list of analysis paths".format(label)
            )
        else:
            for path in grounding:
                if not isinstance(path, str):
                    errors.append("{0}.visual_grounding: paths must be strings".format(label))
                    continue
                ok, value = resolve_path(analysis, path)
                if not ok:
                    errors.append(
                        "{0}.visual_grounding: {1!r} does not resolve in analysis.json".format(
                            label, path
                        )
                    )
                elif value in (None, "", [], {}):
                    errors.append(
                        "{0}.visual_grounding: {1!r} resolves to an empty value".format(
                            label, path
                        )
                    )

        platform = concept.get("platform")
        if platform not in PLATFORMS:
            errors.append(
                "{0}.platform: {1!r} is not one of {2}".format(
                    label, platform, sorted(PLATFORMS)
                )
            )

        valid.append(concept)

    missing_cells = sorted(expected_cells - set(seen_cells))
    if missing_cells:
        preview = ", ".join(missing_cells[:10])
        suffix = " (+{0} more)".format(len(missing_cells) - 10) if len(missing_cells) > 10 else ""
        errors.append(
            "concepts: {0} of {1} cells missing: {2}{3}".format(
                len(missing_cells), len(expected_cells), preview, suffix
            )
        )

    extra = len(concepts) - len(expected_cells)
    if extra > 0:
        warnings.append("concepts: {0} more entries than grid cells".format(extra))

    return valid


def score(concepts: list, analysis: dict) -> dict:
    if not concepts:
        return {"overall": 0, "components": {}}

    hooks = [normalize(c["hook"]) for c in concepts if isinstance(c.get("hook"), str)]
    token_sets = [set(h.split()) for h in hooks if h]
    near_dupes = 0
    total_pairs = 0
    for i in range(len(token_sets)):
        for j in range(i + 1, len(token_sets)):
            a, b = token_sets[i], token_sets[j]
            union = a | b
            if not union:
                continue
            total_pairs += 1
            if len(a & b) / len(union) >= NEAR_DUPLICATE_JACCARD:
                near_dupes += 1
    hook_distinctness = round((1 - near_dupes / total_pairs) * 100) if total_pairs else 100

    paths = []
    multi = 0
    for concept in concepts:
        grounding = concept.get("visual_grounding")
        if isinstance(grounding, list):
            strings = [p for p in grounding if isinstance(p, str)]
            paths.extend(strings)
            if len(strings) >= 2:
                multi += 1
    distinct_paths = len(set(paths))

    available = 0
    for image in analysis.get("images", []) or []:
        if isinstance(image, dict):
            available += len(image)
    rollup = analysis.get("rollup", {}) or {}
    for key, value in rollup.items():
        available += len(value) if isinstance(value, list) else 1
    coverage_target = max(1, min(available, 20))

    platforms = {c.get("platform") for c in concepts if c.get("platform") in PLATFORMS}
    styles = {
        normalize(c["visual_style"])
        for c in concepts
        if isinstance(c.get("visual_style"), str)
    }

    summary_words = []
    for concept in concepts:
        summary = concept.get("summary")
        if isinstance(summary, list):
            for line in summary:
                if isinstance(line, str):
                    summary_words.append(len(words(line)))
    mean_summary = sum(summary_words) / len(summary_words) if summary_words else 0

    components = {
        "hook_distinctness": hook_distinctness,
        "grounding_coverage": min(100, round(distinct_paths / coverage_target * 100)),
        "grounding_depth": round(multi / len(concepts) * 100),
        "platform_spread": min(100, round(len(platforms) / len(PLATFORMS) * 100)),
        "visual_variety": min(100, round(len(styles) / max(1, len(concepts) * 0.5) * 100)),
        "summary_depth": min(100, round(mean_summary / 14 * 100)),
    }
    overall = round(sum(components.values()) / len(components))
    return {"overall": overall, "components": components}


def validate(concepts_path: str, analysis_path: str, min_score: int) -> dict:
    for path in (concepts_path, analysis_path):
        if not Path(path).exists():
            raise FileNotFoundError("Missing file: {0}".format(path))

    data = json.loads(Path(concepts_path).read_text())
    analysis = json.loads(Path(analysis_path).read_text())

    errors: list = []
    warnings: list = []
    formats, angles = validate_grid(data.get("grid"), errors)
    valid = validate_concepts(
        data.get("concepts"), formats, angles, analysis, errors, warnings
    )
    scored = score(valid, analysis)

    if not errors and scored["overall"] < min_score:
        errors.append(
            "score {0} is below --min-score {1}; the weakest components show which "
            "axis collapsed".format(scored["overall"], min_score)
        )

    return {
        "passed": not errors,
        "expected_cells": len(formats) * len(angles),
        "valid_concepts": len(valid),
        "score": scored["overall"],
        "min_score": min_score,
        "components": scored["components"],
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    args = parse_args()
    try:
        result = validate(args.concepts, args.analysis, args.min_score)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
