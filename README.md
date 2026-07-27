# codex-ad

`codex-ad` is a Codex plugin marketplace containing the `ad-maker` plugin.
The plugin bundles an `ad-maker` skill for generating structured static ad
briefs, six-slot image prompts, image reference lists, iteration ladders, and
refinement instructions from campaign context.

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

Open Codex in your campaign folder, then prompt:

```text
Use $ad-maker to create 4 premium static ad prompts for this product.

Brand:
...

Product:
...

Audience:
...

Offer:
...

Assets:
- logo: ./assets/logo.png
- product: ./assets/product.png

Ratio: 4:5
Objective: Conversion
```

For reusable prompt JSON, ask Codex to save the outputs into your campaign
folder.

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
