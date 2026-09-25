# codex-ad

`codex-ad` provides three ad-creative skills for **Codex and ChatGPT Work**.

| Skill | What it does | Start it with |
| --- | --- | --- |
| **`ad-brainstorm`** | Turns one product URL into 100 ad concepts across a 10 format x 10 angle grid, grounded in a shot-by-shot analysis of the product's real photography. | `Run ad-brainstorm on <product URL>` |
| **`ad-maker`** | Turns marketing context into structured static ad prompts, SKU gallery prompt libraries, ordered reference image lists, platform-aware layouts, variants, iteration ladders, readiness scorecards, and post-generation QA refinements. | `Use ad-maker to ...` |
| **`ad-maker2`** | Experimental static generation from researched briefs or finished concepts, with pinned visual-format guides and optional brainstorming. | `Use $ad-maker2 to ...` |

`ad-brainstorm` produces the concepts; `ad-maker` turns a chosen concept into a
production prompt. The package includes all three. The existing ad-brainstorm → ad-maker handoff is unchanged; ad-maker2 is selected explicitly and reuses the bundled ad-maker generation helpers.

No API key is needed for analysis, validation, or native image generation.
`ad-maker` and `ad-maker2` use an available host image generator; the optional
Python API route requires configured API credentials. See [Notes](#notes).

---

## Install and update

This project targets **Codex** and **ChatGPT Work**. Use the prompts below in
those products; you do not need to type commands into a separate terminal.

| Host | Setup scope | How to start a skill |
| --- | --- | --- |
| Codex local app or CLI | Installed plugin, available in new sessions | Select the installed skill or use `$ad-brainstorm`, `$ad-maker`, or `$ad-maker2` |
| ChatGPT Work in the browser | Persistent plugin created through Plugin Creator | Open the returned plugin link, install if prompted, then start a new Work chat |

**ChatGPT Work prerequisite:** enable the **Plugin Creator** plugin and select it
with `@` before sending the Work prompts below. Its connected creation action
uploads a plugin archive and returns a persistent ChatGPT plugin ID and link.
This is different from copying files into a temporary Work session. If Plugin
Creator is unavailable to your account, the prompt must stop with that blocker.

After creation, open the returned link and select **Install** if prompted, then
start a new Work chat. Creation and package read-back have been verified with
Plugin Creator; automatic enablement and skill execution in a fresh browser
chat have not yet been verified. Do not assume creation means installation is
complete. See [ChatGPT plugin usage](https://learn.chatgpt.com/docs/plugins).

### Codex — installation prompt

Paste into a local Codex chat:

```text
Install the codex-ad plugin from https://github.com/markus-404/codex-ad
for my local Codex environment. Perform the setup for me.

Check whether the Codex CLI is available. If it is, run:
codex plugin marketplace add markus-404/codex-ad
codex plugin add codex-ad@codex-ad
codex plugin list

Check that codex-ad@codex-ad is installed and enabled, and report the installed
version. Preserve my other plugins and campaign files. If the required CLI or
permissions are unavailable, report the blocker rather than claiming success.
Tell me to start a new Codex chat to load the three bundled skills:
ad-brainstorm, ad-maker, and ad-maker2.
```

### Codex — update prompt

Paste into a local Codex chat with the plugin already installed:

```text
Update my local codex-ad plugin from markus-404/codex-ad.
First inspect the installed version with codex plugin list and the configured
source with codex plugin marketplace list.
If the source differs from this repository or is intentionally pinned, explain
that before changing it. Otherwise run:
codex plugin marketplace upgrade codex-ad
codex plugin add codex-ad@codex-ad
codex plugin list

Report the previous and resulting versions and any errors. Preserve my other
plugins and campaign files. Do not claim an update if the commands failed.
Tell me to start a new Codex chat to load the updated skills.
```

### ChatGPT Work (browser) — installation prompt

Select **Plugin Creator** with `@`, then paste:

```text
Use Plugin Creator to create a persistent codex-ad plugin from
https://github.com/markus-404/codex-ad in my account. Do the packaging and
creation for me; do not ask me to open Terminal or install Codex CLI.

First check for an existing codex-ad plugin that I own. If one exists, use its
exact ID and the update workflow instead of creating a duplicate. If multiple
matches exist, ask which one to update.

Retrieve a snapshot of main, recording the commit SHA when verifiable. If you
cannot retrieve files, ask me to attach GitHub's Code > Download ZIP archive.
Use only plugins/codex-ad as the plugin package. Keep all three skills and
all their scripts, references, presets, and assets, preserving relative paths.

Use the portable root plugin.json. If the snapshot has only the legacy
.codex-plugin/plugin.json, convert it to Agent Plugins 1.0 with the same name,
version, description, author, and complete interface/defaultPrompt values under
extensions.com.openai. Preserve the compatibility manifest. Do not add an MCP
server or external app dependency.

Package exactly one codex-ad directory as a ZIP, excluding caches and unrelated
repository files. Use Plugin Creator's authenticated creation action to upload
that archive. Do not substitute session files or local marketplace registration.
If the creation action is unavailable or fails, report the actual blocker.

After success, read the saved plugin back and verify the manifest and all three
skills. Return the real plugin link, plugin ID, version, release ID, and creation
status. Tell me whether I still need to click Install and start a new Work chat.
Do not claim automatic enablement or successful skill execution without checking.
```

### ChatGPT Work (browser) — update prompt

Select **Plugin Creator** with `@`. Include the plugin link from installation
if discovery cannot identify it unambiguously.

```text
Use Plugin Creator to update my existing codex-ad plugin from
https://github.com/markus-404/codex-ad. Update the same persistent plugin;
do not create a duplicate or change its sharing.

Resolve its exact plugin ID and read its current source and current release ID.
Retrieve the repository's main snapshot, or ask for its ZIP if retrieval fails.
Compare plugins/codex-ad with the saved release. Preserve my existing metadata,
assets, and integrations unless they are part of this requested upstream update;
explain conflicts or local customizations before overwriting them.

Keep the package name unchanged. Use the portable plugin.json and assign a
strict semantic version greater than the current saved release when content
changes. Synchronize any compatibility manifest. Preserve all starter prompts
and every required resource, including ad-maker2's shared ad-maker files.
If there are no content changes, report that without publishing another release.

Package the updated manifest and changed files. Call Plugin Creator's update
operation with the exact plugin ID and the observed current release ID as the
concurrency guard. If files need deletion, stop and explain: the update operation
overlays files and does not delete omitted files. On a release conflict, reread
and reconcile the current source before retrying. Do not retry an access denial.

After success, read back the saved source and verify the new release and changed
files. Return the same plugin link, old/new versions, and new release ID. Preserve
campaign files and outputs. Tell me to start a new Work chat for the updated skills.
```

Updates are explicit snapshots; a GitHub push does not automatically refresh a
plugin created through Plugin Creator. Each user updates their own copy with the
prompt above. Availability of Plugin Creator and the underlying workflow tools
can vary by account.

### Start creating

After setup, use a real single-product URL:

```text
Use ad-brainstorm on https://example.com/products/my-product.
Return the validated concepts and supporting files as downloads.
```

Or attach a product photo, logo, and brief:

```text
Use ad-maker to generate one Meta feed ad from this brief and the attached
product photo and logo. Use the native image tool.
```

For the experimental alternative:

```text
Use ad-maker2 to generate one static ad from this finished concept and attached
assets. Preserve its copy, claims, audience, and angle. Skip brainstorming.
```

`ad-maker2` is selected explicitly; the normal brainstorm handoff uses `ad-maker`.

| Workflow | Required capabilities |
| --- | --- |
| ad-brainstorm | Page fetching or supplied product material, actual image viewing, shipped scripts, Python execution, writable files, and artifact delivery |
| ad-maker ordinary image | Readable brief/resources, supplied asset viewing, and a native image generator |
| ad-maker production/gallery | Above, plus executable compiler/scorer, PyYAML, and packaged presets |
| ad-maker2 | Applicable ad-maker capabilities plus pinned guide access and actual viewing of format examples |
| Exact product PNG compositing | Actual compositing capability, such as the helper with Pillow |

Missing required tools are blockers, not permission to invent validation scores
or generated outputs. Reference images must actually reach the image tool.
Repository tests do not establish that setup, generation, or downloads work in
your particular Work session.

### Codex — upgrading from 0.1.x

Before 0.2.0, ad-maker shipped as a separate plugin. Ask Codex to remove the old
`ad-maker@codex-ad` install, refresh the `codex-ad` marketplace, and install
`codex-ad@codex-ad`. Preserve campaign files and start a new chat afterward.


## Uninstall

### Codex — uninstall prompt

Paste into Codex:

```text
Uninstall codex-ad@codex-ad from my local Codex environment using:
codex plugin remove codex-ad@codex-ad

Verify the result. Preserve my campaign folders, generated outputs, other
plugins, and marketplace configuration. Tell me to start a new chat or restart
Codex so its skill picker refreshes.
```

To remove only the legacy standalone ad-maker that can cause a duplicate
`ad_maker` entry, ask Codex:

```text
Remove only the legacy ad-maker@codex-ad plugin using:
codex plugin remove ad-maker@codex-ad

Keep codex-ad@codex-ad and all campaign files. Verify removal and tell me to
restart Codex. The current codex-ad plugin already includes ad-maker.
```

If both a GitHub marketplace copy and a Plugin Creator copy are enabled, inspect
their sources in Plugins and uninstall the unwanted copy. Match the source or
plugin ID, not just the shared display name.

### ChatGPT Work (browser)

Open **Plugins**, find your installed **codex_ad**, open its details, and select
**Uninstall plugin**. Use the link returned during creation to identify the
correct copy. Start a new chat afterward.

You can also ask Work, when Plugin Management is available:

```text
Uninstall my codex_ad plugin identified by this plugin link: [paste plugin link].
Resolve that exact plugin before uninstalling. Preserve other plugins, campaign
files, and generated outputs. Report whether uninstall succeeded; do not claim
the underlying created plugin or its release history was deleted.
```

Uninstallation removes the installed bundle from that environment; it should
not be confused with deleting the plugin you created. Separately connected
services are not disconnected by uninstalling a plugin. See the official
[removal instructions](https://learn.chatgpt.com/docs/plugins#remove-a-plugin).


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

In Codex, output lands in your working directory. In browser Work, use a writable
session directory and return the files as downloads:

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

In Codex, open a campaign folder; in browser Work, attach your brief and assets.
The examples below use Codex’s `$ad-maker` notation. In browser Work, write
`Use ad-maker` and refer to attachments instead of local paths:

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
explicitly in ChatGPT Work or `$ad-maker2` in Codex.

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
```

The Codex marketplace is `.agents/plugins/marketplace.json`; its plugin entry
resolves to `plugins/codex-ad`. Packaging tests check the manifests and bundled
resources. Host runtime checks supplement these tests; actual Work-session
setup and image generation require separate end-to-end verification.

## Notes

- `ad-brainstorm` needs no API key at any step.
- Native image generation in `ad-maker` and `ad-maker2` uses the host's existing
  access and limits. Only the explicit Python API route requires
  `OPENAI_API_KEY` in the execution environment; dry-run mode makes no API call.
- Native generation does not promise the API helper's model, size, or quality
  controls. Required unsupported settings must be resolved before generating.
- Product compositing uses Pillow and should only be run on image files from
  trusted campaign folders.
