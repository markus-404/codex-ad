---
name: ad-maker
description: Use when Codex needs to generate or prepare structured static ad images — six-slot prompts, negative prompts, ordered image reference lists, variants, iteration ladders, product compositing instructions, or refinement prompts — from brand, product, persona, scenario, natural-language, or reference-ad inputs.
---

# ad-maker

Use this skill to prepare structured static ad image generation work. Stay inside static ad image generation unless the user explicitly asks for a separate implementation outside this skill.

## Workflow

1. Identify the generation mode: Clone, Iterate, or natural-language brief.
2. Read `references/context-schema.md` before using brand, product, persona, or scenario files.
3. If the user has a rough campaign brief, use `examples/campaign-brief.md` as the shape and `scripts/scaffold_campaign.py` to create starter YAML files.
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
15. Use `scripts/generate_image.py` when the user asks for a dry-run image payload or API execution from compiled prompt JSON.
16. Use `scripts/composite_product.py` when the user asks to preserve exact product appearance by placing a real product PNG onto a generated background.

## Output Contract

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
