# codex-ad

`codex-ad` is one plugin containing three ad-creative skills.

| Skill | What it does | Start it with |
| --- | --- | --- |
| **`ad-brainstorm`** | Turns one product URL into 100 ad concepts across a 10 format x 10 angle grid, grounded in a shot-by-shot analysis of the product's real photography. | `Run ad-brainstorm on <product URL>` |
| **`ad-maker`** | Turns marketing context into structured static ad prompts, SKU gallery prompt libraries, ordered reference image lists, platform-aware layouts, variants, iteration ladders, readiness scorecards, and post-generation QA refinements. | `Use ad-maker to ...` |
| **`ad-maker2`** | Experimental static generation from researched briefs or finished concepts, with pinned visual-format guides and optional brainstorming. | `Use $ad-maker2 to ...` |

`ad-brainstorm` produces the concepts; `ad-maker` turns a chosen concept into a
production prompt. One install delivers all three. The existing ad-brainstorm → ad-maker handoff is unchanged; ad-maker2 is selected explicitly and reuses the bundled ad-maker generation helpers.

No API key is needed for analysis, validation, or native image generation.
`ad-maker` and `ad-maker2` use an available host image generator; the optional
Python API route requires configured API credentials. See [Notes](#notes).

---

## Install

All hosts use this repository: `markus-404/codex-ad`. For teammates in one
ChatGPT workspace, an admin imports the GitHub marketplace once. Available
tools and workspace policies determine which workflows can run.

### ChatGPT and ChatGPT Work — shared workspace

A workspace admin can import the existing skills-only plugin directly from
GitHub. No MCP server, developer-mode connection, or teammate API key is needed
for the native workflow.

1. Open **Admin → Plugins → Add → Import marketplace**.
2. Set **Source** to `https://github.com/markus-404/codex-ad`.
3. Leave **Path** empty: the marketplace is at the repository root. Do not enter
   `.agents/plugins/marketplace.json` or the plugin subdirectory here.
4. Set **Branch, tag, or commit** to `main` for updates, or an approved commit to
   pin a release. Authorize a GitHub account with read access when prompted.
5. Review **Import results**, open `codex-ad`, and set the installation policy
   to **Available** or **Installed** for the intended workspace roles.
6. Teammates select that workspace, install the plugin from **Plugins** if it
   is only Available, and start a new chat with it enabled.

Repository installation/authentication policies do not set workspace role
policies. Admins configure those in ChatGPT. To update after a repository push,
open **Admin → Plugins → Marketplaces**, select the imported marketplace, and
choose **Sync now** (automatic daily sync is also supported). A pinned commit
stays pinned. This workspace import does not publish a public directory listing.

These steps follow the official [workspace plugin management documentation](https://learn.chatgpt.com/docs/enterprise/plugin-management).

Use **Work** for the complete research/100-concept workflow, galleries, and
multi-file deliverables. Chat can handle supported image/prompt requests with
the tools exposed in that session. Type `@` and select the installed plugin or
skill from the picker; naming the skill explicitly in the request also makes
intent clear. Codex's `$skill-name` notation is used in the CLI examples below.

Teammate starter requests:

```text
Use ad-brainstorm on https://example.com/products/my-product.
Return the validated concepts and supporting files as downloads.

Use ad-maker to generate one Meta feed ad from this brief and the attached
product photo and logo. Use the native image tool.

Use ad-maker2 to generate one static ad from this finished concept and attached
assets. Preserve its copy, claims, audience, and angle. Skip brainstorming.
```

Replace the example URL with a real product page; attach approved assets and
supply the brief for the maker requests. No terminal commands or YAML authoring
are needed for ordinary native image requests. `ad-maker2` remains an explicitly
requested alternative; the default brainstorm handoff remains `ad-maker`.

| Workflow | Required capabilities |
| --- | --- |
| ad-brainstorm | Page fetching or supplied product material, actual image viewing, shipped scripts, Python execution, writable files, and artifact delivery |
| ad-maker ordinary image | Readable brief/resources, supplied asset viewing, and a native image generator (or explicitly configured API route) |
| ad-maker production/gallery | Above, plus executable compiler/scorer, PyYAML, and packaged presets |
| ad-maker2 | Applicable ad-maker capabilities plus pinned guide access and actual viewing of format examples |
| Exact product PNG compositing | Actual compositing capability, such as the helper with Pillow; generative editing is not pixel-exact compositing |

Tool availability varies by account, session, and workspace policy. Missing
required tools produce a specific blocker; validation is never replaced by an
invented score. No skill asks teammates to paste API keys into chat. Reference
images must actually reach the generation tool; writing a filename in a prompt
alone does not attach it. Generated images and files are returned through the
host's image/download interface.

The repo includes sandbox execution tests and a [workspace acceptance checklist](docs/chatgpt-workspace-checks.md).
A successful repo test run does not establish that your workspace import,
permissions, native generation, or download links have been tested there.

### Codex

```bash
codex plugin marketplace add markus-404/codex-ad
codex plugin add codex-ad@codex-ad
```

From a local checkout instead of GitHub:

```bash
codex plugin marketplace add .
codex plugin add codex-ad@codex-ad
```

Verify, then start a new chat (or restart Codex Desktop) so the updated skills are available:

```bash
codex plugin list
```

You should see `codex-ad@codex-ad  installed, enabled  0.3.0`.

To pull a newer release later:

```bash
codex plugin marketplace upgrade codex-ad
codex plugin add codex-ad@codex-ad
```

### Claude Code

Works from the shell:

```bash
claude plugin marketplace add markus-404/codex-ad
claude plugin install codex-ad@codex-ad
```

…or from inside a session:

```text
/plugin marketplace add markus-404/codex-ad
/plugin install codex-ad@codex-ad
```

Confirm all three skills registered:

```bash
claude plugin details codex-ad
```

Expected: `Skills (3)  ad-brainstorm, ad-maker, ad-maker2`.

To pull a newer release later:

```bash
claude plugin marketplace update codex-ad
claude plugin update codex-ad
```

Restart the session to apply.

### claude.ai, Claude Desktop, and Cowork

No download, no zip, no terminal. These hosts install the plugin straight from
this GitHub repo, and the bundled skills come with it:

1. Open **Customize** in the left sidebar
2. Go to the **Plugins** tab
3. Under **Personal plugins**, click **+** → **Add marketplace**
4. Choose **Add from a repository** and enter: `markus-404/codex-ad`
5. Install **codex-ad**

Start a new chat and the three skills are available.

There is no chat command that installs a plugin here — `/plugin` works in Claude
Code only, so the five steps above are the whole flow.

`ad-brainstorm` is built for these sandboxes: its scripts are Python stdlib
only, make no network calls, and take explicit file paths. `ad-maker`'s prompt
and scoring workflow requires its packaged files, Python, and PyYAML;
`composite_product.py` additionally needs Pillow. Native image generation is
used when exposed. The optional API helper needs network access and configured
credentials; capabilities are checked rather than assumed from the host name.

### Upgrading from 0.1.x

Releases before 0.2.0 shipped `ad-maker` as its own plugin. 0.2.0 merges it with
`ad-brainstorm` into one `codex-ad` plugin, so the old plugin name no longer
resolves. Remove the old install first:

```bash
# Codex
codex plugin remove ad-maker@codex-ad
codex plugin marketplace upgrade codex-ad
codex plugin add codex-ad@codex-ad
```

```bash
# Claude Code
claude plugin uninstall ad-maker@codex-ad
claude plugin marketplace update codex-ad
claude plugin install codex-ad@codex-ad
```

On claude.ai, Claude Desktop, and Cowork, remove the old `ad-maker` plugin under
**Customize → Plugins**, then install `codex-ad` from the same marketplace.

Nothing in your campaign folders changes — the skill names, script names, and
`output/` layout are all the same.

---

## Skill 1 — `ad-brainstorm`

One product page in, 100 validated ad concepts out.

### Trigger it

```text
Run ad-brainstorm on https://lumora.co/products/vitamin-c-serum
```

It also fires on: *"100 concepts from this URL"*, *"concept grid"*, *"concept
matrix"*, or simply pasting a single product URL and asking for ad concepts. In
Codex you can name it explicitly with `$ad-brainstorm`.

It needs a **single product page URL**. Homepages, category pages, and
collection pages are refused on purpose — the grid is built for one product at a
time.

Optional modifiers, appended to the same message:

| Modifier | Effect |
| --- | --- |
| `Focus on [Meta / TikTok / YouTube]` | Bias the platform recommendations |
| `Target [audience]` | Override the ICP inferred from the page |
| `Skip formats [X, Y]` | Drop archetypes; the expected cell count shrinks with the grid |
| `Generate in [language]` | Localize hooks and summaries; JSON keys stay English |

### What it does

Scrapes the page, looks at up to 5 product photos **shot by shot**, writes an
audience map, then generates one concept per cell of a 10 format x 10 angle
grid. Image analysis uses the host model's own vision — no external vision API,
no key to configure.

Output lands in your working directory:

```
output/[slug]/concepts.json     # source of truth
output/[slug]/concepts.md       # rendered, grouped by format
output/[slug]/audience-map.md
output/[slug]/analysis.json
output/[slug]/scraped.json
output/[slug]/images/
```

### The two quality gates

Both run automatically. You only need these commands to re-check work by hand.

The **analysis gate** enforces per-image detail, a valid color palette, a 4-6
item gap list, exactly 5 suggested visual styles, and consistency between "no
humans shown" and a flagged UGC gap. It also rejects an analysis where every
photo got an identical read — the tell that the images were never looked at
individually:

```bash
python3 plugins/codex-ad/skills/ad-brainstorm/scripts/validate_analysis.py \
  --analysis output/vitamin-c-serum/analysis.json
```

The **concept gate** enforces full grid coverage, IDs that match their cell,
unique hooks under 15 words, exactly 2 summary lines, and — the important one —
that every concept's `visual_grounding` resolves to a real path inside
`analysis.json`. No concept can claim image grounding it does not have:

```bash
python3 plugins/codex-ad/skills/ad-brainstorm/scripts/validate_concepts.py \
  --concepts output/vitamin-c-serum/concepts.json \
  --analysis output/vitamin-c-serum/analysis.json
```

Each gate returns a 0-100 score with a component breakdown and blocks below
`--min-score` (default 75). Reading the components:

- low `grounding_coverage` — the image layer was decorative, not load-bearing
- low `visual_variety` — one treatment got recycled across cells
- low `hook_distinctness` — the format and angle axes collapsed into each other

`concepts.json` is the source of truth; `concepts.md` is rendered from it and
should never be hand-edited:

```bash
python3 plugins/codex-ad/skills/ad-brainstorm/scripts/render_concepts.py \
  --concepts output/vitamin-c-serum/concepts.json \
  --out output/vitamin-c-serum/concepts.md
```

### Chain into `ad-maker`

Hand a concept's `hook` and `visual_style` to `ad-maker` to compile a real
prompt. Both skills ship together, so this needs no extra install.

---

## Skill 2 — `ad-maker`

Marketing context in, production-ready static ad prompts and SKU galleries out.

### Trigger it

Open your host in any campaign folder and write plain text. In Codex, `$ad-maker`
names the skill explicitly:

```text
Use $ad-maker to make a Meta feed ad for this product.

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

It picks a preset, produces a structured prompt, preserves logo and product
reference order, and suggests refinements. It also activates on any request to
generate or prepare static ad images, variants, iteration ladders, or refinement
prompts.

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

Create a SKU gallery prompt library:

```text
Use $ad-maker to create a 4-6 image Shopee gallery prompt library for this SKU.
Score every prompt before generation and write post-generation QA refinements.
```

### Platform presets

- `meta-feed-conversion`
- `instagram-story`
- `square-retargeting`
- `tiktok-static`
- `linkedin-lead-gen`

### Deterministic helper scripts

The skill runs these for you; the paths below are for running them by hand from
a checkout of this repo.

Repeatable campaign setup:

```bash
python3 plugins/codex-ad/skills/ad-maker/scripts/scaffold_campaign.py \
  --brief examples/campaign-brief.md \
  --out-dir campaigns/sample-foods
```

Preset-aware prompt JSON:

```bash
python3 plugins/codex-ad/skills/ad-maker/scripts/compile_prompt.py \
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

Deterministic quality scoring:

```bash
python3 plugins/codex-ad/skills/ad-maker/scripts/score_prompt.py \
  --prompt-json campaigns/sample-foods/prompt.json
```

Dry-run image request payload:

```bash
python3 plugins/codex-ad/skills/ad-maker/scripts/generate_image.py \
  --prompt-json campaigns/sample-foods/prompt.json \
  --out-dir campaigns/sample-foods/images \
  --dry-run
```

---

## Skill 3 — `ad-maker2`

Explicitly invoke the experimental skill with a researched product brief or a
finished concept:

```text
Use $ad-maker2 to generate a static Meta feed ad from this finished concept.
Preserve the supplied copy, claims, audience, and angle; apply a compatible
visual format to its layout and visual treatment.
```

A clear brief goes directly to format-guided prompt/image generation.
Brainstorming is an add-on only when creative direction is missing or requested.
It does not scrape product URLs or replace the existing skills or their handoff.
Automatic invocation is disabled in its OpenAI skill metadata; use ad-maker2
explicitly in ChatGPT/Work or `$ad-maker2` in Codex.

The skill fetches classification/execution guides and visually studies examples
from [Visual Formats at commit 498444b](https://github.com/alyshadotmd/visual-formats/tree/498444b7fdc4da674f07d8b0432c32a24b5062c9).
Every concept uses a documented still-compatible format. Outputs include source
receipts and format-specific checks alongside the existing prompt/image outputs.
Pinned-source access (or a provenance-verified cache/resource), image viewing,
and the bundled ad-maker resources are required. Missing sources or incompatible fixed inputs
are reported instead of silently bypassing the format requirements. Image generation
uses the shared native/API routing. Native tools may expose different controls
from the API; unsupported exact settings are reported before generation.

The skill does not establish better ad performance or include a comparison harness.

---

## Develop and validate

```bash
python3 -c 'import sys, importlib; pytest=importlib.import_module("pytest"); sys.exit(pytest.main(["-q"]))'
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/codex-ad
claude plugin validate .
claude plugin validate plugins/codex-ad
```

Two marketplace manifests must stay in sync — `.claude-plugin/marketplace.json`
for Claude Code and `.agents/plugins/marketplace.json` for Codex and ChatGPT
workspace import. The test suite
enforces that they agree and that both resolve to real plugin directories.

## Notes

- `ad-brainstorm` needs no API key at any step.
- Native image generation in `ad-maker` and `ad-maker2` uses the host's existing
  access and limits. Only the explicit Python API route requires
  `OPENAI_API_KEY` in the execution environment; dry-run mode makes no API call.
- Native generation does not promise the API helper's model, size, or quality
  controls. Required unsupported settings must be resolved before generating.
- Product compositing uses Pillow and should only be run on image files from
  trusted campaign folders.
