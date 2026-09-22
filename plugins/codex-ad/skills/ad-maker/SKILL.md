---
name: ad-maker
description: Use when the user requests static ad images or prompts, variants, SKU galleries, product compositing, or refinements from a brief, product assets, or reference ad in ChatGPT, ChatGPT Work, Codex, or Claude.
---

# ad-maker

Use this skill to prepare structured static ad image generation work. Stay inside static ad image generation unless the user explicitly asks for a separate implementation outside this skill.

## Host capabilities and files

Read [generation runtime](references/generation-runtime.md) first. Use available host tools rather than assuming a terminal, API credentials, local paths, or a particular image model. In ChatGPT and ChatGPT Work, accept the brief and approved product/logo images as attachments; use the native image tool when available for image requests. Prompt-only requests do not trigger generation.

Read supporting files through the host's skill-resource mechanism or the actual installed directory. Resolve exact resource identifiers from the host; never treat a `skill://` URI as a filesystem path. Use paths below relative to this skill for filesystem installs. Stage actual packaged files only when a Python helper requires them. Deliver created files through the host's download/artifact mechanism; local filesystem paths alone are not a ChatGPT handoff.

## Workflow

1. Identify the generation mode: Clone, Iterate, or natural-language brief.
2. Read `references/context-schema.md` before using brand, product, persona, or scenario files.
3. Accept a clear natural-language brief directly. If reusable campaign files are requested, use [campaign brief](examples/campaign-brief.md) as the shape and `scripts/scaffold_campaign.py` to create starter YAML files. Do not require teammates to write YAML for ordinary image requests.
4. Read `references/platform-presets.md` when the user names a channel, placement, or goal. Use a preset instead of asking for raw aspect ratios when possible.
5. Read `references/prompt-template.md` before writing any generation prompt. Write the `Visual` and `Layout` slots yourself for every prompt, and vary them across a variant set.
6. Read `references/generation-modes.md` when a request names Clone, Iterate, reference ads, variants, or natural-language ad generation.
7. Read `references/iteration-ladder.md` for requests that turn one winning ad into multiple concepts.
8. Read `references/taxonomies.md` for archetype, objective, ratio, copy-framework, or creative-tag choices.
9. Read `references/product-fidelity.md` when exact product appearance matters.
10. Read `references/sku-gallery-library.md` for production prompt libraries, SKU-level prompt sets, Shopee galleries, product detail page galleries, or 4-6 image prompt batches.
11. Read `references/refinement-workflows.md` for reuse, vary, text edit, inpaint, or post-generation QA requests.
12. Use `scripts/compile_prompt.py` when the user asks for deterministic prompt JSON or reusable prompt files. Prefer `--platform-preset` over asking marketers to provide ratios. Pass your authored slots with `--visual` and `--layout`; omitting them falls back to generic template wording that is not suitable for a delivered ad.
13. Use `scripts/score_prompt.py` when the user asks for quality review, readiness checks, or recommendations before image generation. For production, gallery, Shopee, or multi-prompt SKU batches, scoring is a normal gate: score every compiled prompt JSON and revise anything below 75 before generating or handing off.
14. Use `scripts/create_iteration_ladder.py` when the user asks to turn one winning ad into strategies and ad ideas.
15. For image requests, follow [generation runtime](references/generation-runtime.md) and return actual generated images when the needed tools and inputs are available. Use `scripts/generate_image.py` for explicit dry-run/API requests or an available configured local API workflow; native image generation does not require an API key. Required scoring gates still apply on every route.
16. Use `scripts/composite_product.py` when the user asks to preserve exact product appearance by placing a real product PNG onto a generated background.

## Output Contract

For image-generation requests, return the generated images with a short account of the actual route, reference assets used, requested versus supported settings, and visual QA results. Also retain the prompt records below as reusable files or concise accompanying content. If generation or a required gate is blocked, name that blocker and label any preparatory output as a draft, not a completed image.

For prompt-generation requests, return:
- prompt
- negative prompt
- ordered reference image list
- mode
- objective
- ratio
- platform preset
- variant count
- lineage metadata
- quality score and revision recommendations when scoring is requested or when the request is production/gallery/SKU work
- next refinement options

For production gallery or SKU-library requests, return:
- 4-6 prompt records in gallery order
- slot purpose for each image
- compiled prompt JSON path or payload for each slot
- readiness score for each slot
- ordered reference image list for each slot
- generation notes and post-generation QA checklist
- refinement instruction for each failed QA item

For iteration-ladder requests, return:
- original ad summary
- performance notes
- 3 strategies
- 12 total ad ideas
- next prompt-generation options

For product-fidelity requests, preserve the supplied logo and product references by index. Recommend real product PNG compositing when exact product shape, label geometry, cap shape, package proportions, or material appearance must not drift.

## Exclusions

Do not perform ad-library scraping, paid-media analytics, bulk launch tooling, full layered raster editing, or full third-party app/UI cloning.
