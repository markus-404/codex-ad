---
name: ad-brainstorm
description: Takes a single product URL, scrapes the product page, analyzes the real product photography shot by shot, builds an audience map, then generates 100 ad concepts across a 10 format x 10 angle grid. Each concept carries a hook line, 2-line summary, visual direction cited back to a specific image observation, and a recommended platform. Deterministic validators enforce grid coverage, unique hooks, and image grounding before anything ships. Use when the user says "run ad-brainstorm", "brainstorm ad concepts", "url to 100 concepts", "100 concepts from this URL", "concept grid", "concept matrix", or pastes a single product page URL and asks for ad concepts, creative concepts, or campaign ideas.
---

# ad-brainstorm — One URL to 100 Concepts

Runs in Claude Code, Codex, Claude.ai, and Cowork. The image analysis uses the
host model's own vision — there is no external vision API and no API key to set up.

## When to Activate

- User says "run ad-brainstorm", "brainstorm ad concepts", "url to 100 concepts", "100 concepts from this URL"
- User pastes a single product page URL and asks for ad concepts, creative concepts, or campaign ideas
- User mentions "concept grid", "concept matrix", or "100 ad ideas"

## Paths

Two path roots are used below and they are not the same thing:

- **`$SKILL_DIR`** — the directory holding this SKILL.md, with `references/` and
  `scripts/` beside it. Resolve it once at the start and reuse it. It is
  `${CLAUDE_PLUGIN_ROOT}/skills/ad-brainstorm` in Claude Code, the installed
  plugin's skill path in Codex, and the uploaded skill folder on claude.ai. Never
  assume it is under the user's working directory — an installed plugin is not.
- **`output/[slug]/`** — relative to the user's current working directory. This is
  their deliverable and belongs in their project, never inside `$SKILL_DIR`.

The scripts take explicit `--analysis` / `--concepts` / `--out` paths and never
read the working directory, so only the script path itself needs resolving.

## Workflow

### 1. Confirm the input

Require a **single product page URL**. For a homepage, category, or collection page, reply:

> I need a specific product page URL. The skill generates 100 concepts for ONE product at a time.

Do not proceed.

Derive the **slug**: strip the query string and fragment, take the last path segment,
lowercase it, collapse non-alphanumerics to hyphens. `.../products/vitamin-c-serum?variant=42`
→ `vitamin-c-serum`. If that segment is generic (`index`, `product`, a bare numeric ID),
slugify the scraped product title instead. Every output path below uses this slug.

### 2. Scrape the page

Read `references/scrape-routes.md` and work the routes in order. Route A is host-native
and works in every environment; B and C are shell fallbacks that produce better image URLs
where a shell with network access exists.

Save the result to `output/[slug]/scraped.json`. On total failure, stop and ask the user
to paste the details — never proceed on empty data.

### 3. Look at the product images

Get up to 5 images in front of yourself — download to `output/[slug]/images/` and read
them, or view them directly. `references/scrape-routes.md` covers the options per host.

**You must actually view the images.** If this environment cannot display images to you,
say so and ask the user to paste them. Do not infer a visual analysis from the product
copy, the brand name, or the category — that failure mode is exactly what this step exists
to prevent, and it is invisible in the output once it happens.

### 4. Write the analysis

Read `references/vision-schema.md`. Write `output/[slug]/analysis.json` with a **per-image**
entry for every photo you viewed plus a **rollup** across the set.

Per-image first, rollup second. The rollup's `whats_missing` and `ugc_opportunity` are the
highest-value fields in the file — they are what let a concept propose something the brand
has never shot. They only get sharp if the per-image reads were specific first.

### 5. Validate the analysis — hard gate

```bash
python3 "$SKILL_DIR/scripts/validate_analysis.py" \
  --analysis output/[slug]/analysis.json
```

Exit 0 to continue. On failure the script prints every violation with a field path and a
score breakdown. Fix the named fields and re-run. Do not proceed past a red gate, and do not
lower `--min-score` to get through it — the score measures whether the analysis is specific
enough to ground 100 distinct concepts, which is the whole premise of the skill.

### 6. Present the intelligence

Show the user:

- **Scraped:** product / price / brand / benefits / review quotes / brand voice
- **Analysis:** form factor / palette / packaging style / brand aesthetic / who is in the photos / what's missing / suggested visual styles / UGC opportunity
- **Validation:** score and component breakdown

Then ask: *"Look good? I'll generate 100 concepts across a 10x10 format/angle grid."*

### 7. Build the audience map

From the scraped copy, reviews, and the aesthetic read, generate 3-5 ICP segments. For each:

- Name + one-line profile
- Top 3 pains, in their voice
- Top 3 desires, in their voice
- 5 phrases they actually use
- Which analysis-identified visual direction fits them best

Write `output/[slug]/audience-map.md`.

### 8. Generate the grid — one format at a time

Read `references/grid.md` for the axes and `references/concept-schema.md` for the record shape.

**Generate in 10 batches of 10, one format archetype per batch.** Do not attempt all 100 in
a single pass — that is what produces collapsed output where the format and angle axes blur
together. After each batch, append to `output/[slug]/concepts.json` and check the new hooks
against every hook already written.

Each concept cites `visual_grounding` — one or more paths into `analysis.json`
(`images[2].lighting`, `rollup.ugc_opportunity`, `rollup.suggested_visual_styles[3]`).
The validator resolves every path, so a concept cannot claim grounding it does not have.
Spread the citations: a run where all 100 concepts cite the same field scores near zero on
`grounding_coverage`, and correctly so.

### 9. Validate the concepts — hard gate

```bash
python3 "$SKILL_DIR/scripts/validate_concepts.py" \
  --concepts output/[slug]/concepts.json \
  --analysis output/[slug]/analysis.json
```

Hard failures: missing or duplicated cells, IDs that disagree with their format/angle,
duplicate hooks, hooks over 15 words, summaries that are not exactly 2 lines, unresolvable
grounding paths, unknown platforms, placeholder text.

Score components name the axis that collapsed. `hook_distinctness` low means the hooks are
rewordings of each other. `visual_variety` low means one visual style got recycled.
`grounding_coverage` low means the image layer was decorative. Regenerate the affected
cells — not the whole grid — and re-run.

### 10. Render and summarize

```bash
python3 "$SKILL_DIR/scripts/render_concepts.py" \
  --concepts output/[slug]/concepts.json \
  --out output/[slug]/concepts.md
```

Final tree:

```
output/[slug]/concepts.json     # source of truth
output/[slug]/concepts.md       # rendered, grouped by format
output/[slug]/audience-map.md
output/[slug]/scraped.json
output/[slug]/analysis.json
output/[slug]/images/
```

Then report:

```
100 concepts generated and validated.
Product: [title] | Formats: 10 | Angles: 10 | Total: 100
Analysis score: [N]/100 | Concept score: [N]/100
Output: output/[slug]/

Top 5 Picks (biggest UGC gap + highest-signal formats):
  1. [Concept ID] — [hook]
  2. ...
```

### 11. Offer to chain

To turn a concept into a static ad prompt, hand the `visual_style` and `hook` to the
**ad-maker** skill — it compiles platform-aware six-slot prompts and scores them.
ad-maker ships in the same `codex-ad` plugin, so it is normally already available.
If it is not, say so rather than guessing at its interface. This skill has no hard
dependency on it.

## Hard Rules

- Never invent the image analysis. If you cannot see the images, stop and ask.
- Never skip a validator, and never relax `--min-score` to pass one.
- `concepts.json` is authored; `concepts.md` is rendered. Never hand-write the markdown.
- Never reuse a hook line. 100 concepts means 100 distinct hooks.
- Concept IDs must map to the real cell.
- No filler. Each concept must be shippable as a brief on its own.

## Input Template

```
Run ad-brainstorm on [PRODUCT URL]
```

Optional modifiers — see `references/grid.md`:

- `Focus on [Meta / TikTok / YouTube]` — bias platform recommendations
- `Target [audience]` — override the scraped ICP
- `Skip formats [X, Y]` — exclude archetypes; expected cell count shrinks with the grid
- `Generate in [language]` — hooks and summaries localized; JSON keys stay English

## Exclusions

No ad-library scraping, paid-media analytics, bulk launch tooling, or image generation.
Image generation belongs to ad-maker.
