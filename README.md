# codex-ad

`codex-ad` is a Codex plugin marketplace containing the `ad-maker` plugin.
The plugin bundles an `ad-maker` skill for turning normal marketing context into
structured static ad prompts, image reference lists, platform-aware layouts,
iteration ladders, and deterministic quality scorecards.

## Install

From a public GitHub repo:

```bash
codex plugin marketplace add markus-404/codex-ad
codex plugin add ad-maker@codex-ad
```

From a local checkout:

```bash
codex plugin marketplace add .
codex plugin add ad-maker@codex-ad
```

Restart Codex Desktop or start a new chat after installation so the bundled
skill is available.

## Use

Open Codex in any campaign or work folder. A marketer can start with plain text:

```text
Use $ad-maker to make a nice enough Meta feed ad for this product.

Brand:
Sample Foods

Product:
Sample Bottle, a premium ready-to-use sauce for fast weeknight dinners.

Audience:
Busy adults who want better dinners without complicated prep.

Offer:
Save 20% today

Assets:
- logo: ./assets/logo.png
- product: ./assets/product.png
```

The skill will choose a preset, produce a structured prompt, preserve the logo
and product reference order, and suggest the next refinement options.

### Quickstarts by use case

Create a conversion ad:

```text
Use $ad-maker to create 4 static ad prompt variants for a Meta feed conversion
campaign. Use product-forward layouts and keep copy short.
```

Create an Instagram story ad:

```text
Use $ad-maker to create a vertical story ad from this brief. Use the
instagram-story preset and keep product and text inside safe zones.
```

Turn a rough brief into reusable files:

```text
Use $ad-maker to scaffold campaign files from examples/campaign-brief.md, then
compile one prompt JSON using the best preset.
```

Improve an existing winning ad:

```text
Use $ad-maker to create an iteration ladder from this winning ad: [paste notes].
Then turn the strongest three ideas into prompt JSON.
```

Quality-check before image generation:

```text
Use $ad-maker to score this prompt JSON and revise anything below 75 before
generating images.
```

### Deterministic helper scripts

For repeatable campaign setup:

```bash
python3 plugins/ad-maker/skills/ad-maker/scripts/scaffold_campaign.py \
  --brief examples/campaign-brief.md \
  --out-dir campaigns/sample-foods
```

For preset-aware prompt JSON:

```bash
python3 plugins/ad-maker/skills/ad-maker/scripts/compile_prompt.py \
  --brand campaigns/sample-foods/brand.yaml \
  --product campaigns/sample-foods/product.yaml \
  --persona campaigns/sample-foods/persona.yaml \
  --scenario campaigns/sample-foods/scenario.yaml \
  --mode brief \
  --objective Conversion \
  --platform-preset meta-feed-conversion \
  --variant-count 4 \
  --headline "Simple dinners, better flavor" \
  --subline "Chef-level sauce for busy weeknights" \
  --offer "Save 20% today" \
  --out campaigns/sample-foods/prompt.json
```

For deterministic quality scoring:

```bash
python3 plugins/ad-maker/skills/ad-maker/scripts/score_prompt.py \
  --prompt-json campaigns/sample-foods/prompt.json
```

For a dry-run image request payload:

```bash
python3 plugins/ad-maker/skills/ad-maker/scripts/generate_image.py \
  --prompt-json campaigns/sample-foods/prompt.json \
  --out-dir campaigns/sample-foods/images \
  --dry-run
```

Available platform presets:

- `meta-feed-conversion`
- `instagram-story`
- `square-retargeting`
- `tiktok-static`
- `linkedin-lead-gen`

## Validate

```bash
python3 -c 'import sys, importlib; pytest=importlib.import_module("pytest"); sys.exit(pytest.main(["-q"]))'
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/ad-maker
```

If your skill validator lives elsewhere, locate it with:

```bash
find "$HOME/.codex" -path "*/skill-creator/scripts/quick_validate.py" -print -quit
```

## Notes

- Real image generation requires `OPENAI_API_KEY`.
- Dry-run mode does not call the OpenAI API.
- Product compositing uses Pillow and should only be run on image files from
  trusted campaign folders.
