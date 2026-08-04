# Concept Schema

`concepts.json` is the source of truth. `concepts.md` is rendered from it by
`scripts/render_concepts.py` — never hand-write the markdown, it will drift.

`scripts/validate_concepts.py` enforces every rule below against `concepts.json`
and cross-checks grounding paths against `analysis.json`.

## Shape

```json
{
  "product": {
    "title": "Lumora Vitamin C Brightening Serum",
    "brand": "Lumora",
    "price": "$48",
    "url": "https://lumora.co/products/vitamin-c-serum",
    "slug": "vitamin-c-serum"
  },
  "grid": {
    "formats": ["UGC monologue", "Before/after timer", "..."],
    "angles": ["Pain killer", "Status symbol", "..."]
  },
  "concepts": [
    {
      "id": "F1-A1",
      "format_index": 1,
      "format": "UGC monologue",
      "angle_index": 1,
      "angle": "Pain killer",
      "hook": "I had three serums pilling under my SPF. One didn't.",
      "summary": [
        "Selfie cam, messy morning bathroom, three bottles lined up on the counter.",
        "She rubs each into the back of her hand; only the Lumora stays smooth."
      ],
      "visual_style": "Warm morning bathroom, natural window light, raw handheld",
      "visual_grounding": ["rollup.suggested_visual_styles[1]", "rollup.ugc_opportunity"],
      "platform": "Meta Reels"
    }
  ]
}
```

## Rules

**Grid coverage**
- `grid.formats` and `grid.angles` define the expected cell count: `len(formats) × len(angles)`.
- Default is 10 × 10 = 100. `Skip formats [X, Y]` shrinks `formats`, and the expected count shrinks with it — the validator never hard-codes 100.
- Every cell `F{i}-A{j}` must appear exactly once. Missing cells and duplicate cells both fail.
- `id` must equal `F{format_index}-A{angle_index}`.
- `format` must equal `grid.formats[format_index - 1]`, `angle` must equal `grid.angles[angle_index - 1]`. This is what makes an ID traceable rather than decorative.

**Hooks**
- Non-empty, ≤ 15 words.
- Unique after normalization (lowercased, punctuation stripped, whitespace collapsed). 100 concepts means 100 distinct hooks.
- Near-duplicate pairs (token Jaccard ≥ 0.7) do not hard-fail but pull the score down — that is the "grid axes collapsed into each other" failure showing up as a number.

**Summary**
- Exactly 2 lines, each ≥ 6 words. Two lines is the brief; one line is a slogan and three is a treatment.

**Visual grounding**
- `visual_style` ≥ 4 words.
- `visual_grounding` is a non-empty array of paths that must resolve in `analysis.json`.
- This is the enforcement of "every concept must be grounded in the image analysis". Previously prose, now a resolvable reference.

**Platform**
- ∈ `Meta feed`, `Meta Reels`, `TikTok`, `YouTube Shorts`, `YouTube long-form`, `Reddit`, `LinkedIn`, `Pinterest`.

**Anti-filler**
- Placeholder text (`TODO`, `TBD`, `N/A`, `lorem`, `placeholder`, `example hook`) fails anywhere.

## Score components

The validator returns a 0–100 score alongside pass/fail. Structural rules above
are hard failures; these are quality signals, gated by `--min-score` (default 75):

| Component | What it measures |
|---|---|
| `hook_distinctness` | Share of hook pairs that are not near-duplicates |
| `grounding_coverage` | Distinct analysis paths cited across the whole set — if all 100 concepts cite one field, the image layer was decorative |
| `grounding_depth` | Share of concepts citing 2+ paths |
| `platform_spread` | Distinct platforms used, against the 8 available |
| `visual_variety` | Distinct normalized `visual_style` strings |
| `summary_depth` | Mean words per summary line |

A run can be structurally perfect and still score badly. That is the point:
100 valid rows with 3 recycled visual styles is a failed brainstorm, not a passing one.
