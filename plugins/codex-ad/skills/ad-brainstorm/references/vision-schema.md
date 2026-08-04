# Vision Analysis Schema

`analysis.json` is the output of looking at the product photos. It has two parts:
a **per-image** read (one entry per photo, so per-shot detail survives) and a
**rollup** (the cross-photo synthesis, including the gap analysis).

`scripts/validate_analysis.py` enforces every rule below. A run that fails
validation cannot proceed to concept generation.

## Shape

```json
{
  "images": [
    {
      "index": 1,
      "source_url": "https://cdn.example.com/hero.jpg",
      "shot_type": "hero",
      "subject": "what is actually in frame, specifically",
      "form_factor": "shape, proportion, size impression, closure type",
      "materials_finish": "glass/plastic/paper, matte/gloss/soft-touch, opacity",
      "label_and_typography": "label geometry, type style, weight, case, alignment",
      "color_hexes": ["#f4ede3", "#8b6a3f"],
      "lighting": "direction, hardness, temperature, visible falloff",
      "camera_angle": "eye-level 3/4, top-down flat-lay, low hero, macro",
      "backdrop_surface": "what the product sits on and what is behind it",
      "humans": "no humans shown",
      "props": ["dried botanicals", "linen cloth"],
      "mood": "quiet clinical calm"
    }
  ],
  "rollup": {
    "form_factor": "the consensus physical read across all shots",
    "color_palette": ["#f4ede3", "#8b6a3f", "#ffffff"],
    "packaging_style": "minimal",
    "brand_aesthetic_read": "one sentence on the vibe this brand projects visually",
    "who_is_in_the_photos": "no humans appear in any of the 6 images",
    "settings_shown": "every environment and backdrop used across the set",
    "premium_or_playful": "premium",
    "whats_missing": ["4 to 6 visual territories the photoset never enters"],
    "suggested_visual_styles": ["exactly 5 specific, shootable directions"],
    "ugc_opportunity": "the single biggest UGC-style angle the photoset is missing"
  }
}
```

## Rules

**Images**
- 1–5 entries. Fewer than 3 passes but scores lower — 3+ is where cross-shot gap analysis gets reliable.
- `index` is 1-based and must be unique.
- `shot_type` ∈ `hero`, `lifestyle`, `detail`, `macro`, `packaging`, `in-use`, `scale`, `comparison`, `ingredient`, `other`.
- `color_hexes`: at least 2 valid `#rrggbb` values per image.
- Every prose field must clear a minimum word count (see `MIN_WORDS` in the validator). This is what stops one-word answers like "white" or "studio".
- `humans` accepts `no humans shown` / `none` as a real answer — it is often the most valuable observation in the whole file.
- The set of `(shot_type, camera_angle, lighting)` triples must not be identical across all images. Five identical reads means the photos were not actually looked at individually.

**Rollup**
- All 10 fields required.
- `color_palette`: at least 3 valid `#rrggbb` values.
- `packaging_style` ∈ `matte`, `glossy`, `minimal`, `maximalist`, `retro`, `editorial`, `clinical`, `playful`.
- `premium_or_playful` ∈ `premium`, `playful`, `clinical`, `editorial`, `utilitarian`.
- `whats_missing`: 4–6 items, each ≥ 3 words.
- `suggested_visual_styles`: exactly 5 items, each ≥ 3 words.
- Placeholder text (`TODO`, `TBD`, `N/A`, `unknown`, `lorem`, `describe...`, `example`) fails anywhere in the file.

**Consistency**
- If `who_is_in_the_photos` indicates no humans, then `whats_missing` or `ugc_opportunity` must mention people, humans, faces, hands, skin, or UGC. A photoset with no humans and no flagged human gap means the gap analysis was not done.

## Grounding paths

Concepts cite analysis elements by path. These resolve against `analysis.json`:

```
images[0].lighting
images[2].backdrop_surface
rollup.ugc_opportunity
rollup.suggested_visual_styles[3]
rollup.whats_missing[1]
```

`images[N]` is 0-based array position, not the `index` field. `validate_concepts.py`
resolves every path and fails on any that does not exist or points at an empty value.
