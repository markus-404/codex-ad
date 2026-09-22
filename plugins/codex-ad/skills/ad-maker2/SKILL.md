---
name: ad-maker2
description: Use when the user explicitly requests ad-maker2 for static ad generation or optional creative brainstorming from an already researched product brief or finished concept.
---

# ad-maker2

An experimental alternative to ad-maker: the same static generation foundation, with mandatory Visual Formats guidance and optional brainstorming. Invoke only when explicitly requested. Work from supplied research; do not run product research or redirect the existing ad-brainstorm handoff.

## Installed paths and shared foundation

Read [generation runtime](../ad-maker/references/generation-runtime.md) for ChatGPT, ChatGPT Work, and local generation/file handling. Both skills ship in codex-ad. On filesystem installs, resolve this file's directory as `AD_MAKER2_DIR` and its sibling `../ad-maker` as the absolute `AD_MAKER_DIR`; shared references/scripts resolve there. In resource-backed sessions, discover the bundled ad-maker resources through the host's actual skill metadata/reader and use their returned identifiers. Do not assume cloud sibling paths or convert resource URIs into paths. Materialize required scripts/resources only for Python execution; stop the affected step if unavailable. CLI input/output paths belong to the user's project/session; image paths inside brand/product YAML remain relative to the containing YAML file or absolute.

Read the [baseline workflow and output contracts](../ad-maker/SKILL.md) as shared documentation, without invoking that skill or changing its files. Retain its modes, six-slot prompts, negative prompts, ordered references, presets, product fidelity, conditional scoring, generation helpers, and requested refinements. The rules below take precedence over baseline ideation and copy-edit instructions. Accept researched briefs and approved product/logo attachments directly; do not require campaign YAML for ordinary generation.

## Route the brief

- **Generation-ready brief or selected concept:** skip brainstorming and proceed through format selection to the requested prompt or image generation. Do not expand it into strategies or twelve ideas, including in Iterate mode, unless requested.
- **Researched brief needing creative development:** brainstorm only enough to resolve the missing creative direction or fulfill the requested concept count. Apply the format procedure below to each concept before presenting it. Provide the format, angle, proposed copy, visual direction, and reason it fits the supplied facts. No mandatory 100-concept grid or extra approval step.
- **Missing essential facts or assets:** ask for those inputs. Brainstorming cannot supply product evidence, testimonials, statistics, offers, or unseen product details.

For finished concepts, preserve supplied copy verbatim, claims, audience, and angle. Change layout and visual treatment only. For rough briefs, develop only unspecified creative elements from verified inputs. If a format requires different copy, additional claims, or incompatible brand treatment, choose a compatible format or explain the conflict and ask; never silently rewrite the brief. This also overrides the baseline readability exception: fix typography/layout, not approved wording.

## Apply formats, then generate

1. Follow [pinned format retrieval](references/visual-formats.md) before brainstorming or prompt authoring. Every concept must use a documented, still-image-compatible format. Read its classification and execution guides and visually inspect its example creative(s). Carry applicable execution rules into the actual composition and copy treatment; a format label alone is insufficient.
2. Use the shared [prompt template](../ad-maker/references/prompt-template.md). Author Visual and Layout from the chosen execution guide; keep brand and exact copy constraints in the remaining slots. Read [context schema](../ad-maker/references/context-schema.md) for structured inputs, [platform presets](../ad-maker/references/platform-presets.md) for placements, and [product fidelity](../ad-maker/references/product-fidelity.md) for supplied assets.
3. For requested modes or batch work, read [generation modes](../ad-maker/references/generation-modes.md), [iteration ladder](../ad-maker/references/iteration-ladder.md), or [SKU galleries](../ad-maker/references/sku-gallery-library.md) as applicable. Their output shapes remain, except ready concepts bypass unrequested ideation. Baseline archetype tags are separate from the upstream visual-format token.
4. Follow [generation runtime](../ad-maker/references/generation-runtime.md): use an exposed native image tool for image requests, binding approved attachments and including negative constraints. No API key is needed for that route. Reuse [compile_prompt.py](../ad-maker/scripts/compile_prompt.py), [score_prompt.py](../ad-maker/scripts/score_prompt.py), [generate_image.py](../ad-maker/scripts/generate_image.py), and [composite_product.py](../ad-maker/scripts/composite_product.py) where applicable and executable. Pass authored Visual/Layout slots. Preserve scoring gates and requested counts; honor settings the route supports, and resolve mandatory unsupported controls before generation. Do not claim native model/settings match API defaults without evidence or add automatic rerolls. If generation was requested and inputs/tools are available, carry it through. Report unavailable access plainly.
5. Before generation, check the prompt against the selected guide's applicable anatomy, copy caps, medium constraints, and QA requirements, plus fixed brief inputs. After generation, inspect the images using [baseline QA](../ad-maker/references/refinement-workflows.md) and those same format requirements. Record failures and targeted refinements; do not claim a prompt-only or dry-run check validates rendered images.

## Deliver

Keep the baseline output contract for the requested task. Add a concise format receipt per concept/image: format token(s), pinned commit, guide URLs, inspected example paths/URLs or host resource identifiers, applied execution rules, and prompt/render QA results (pass, fail, or not checked, with reasons). Keep receipts alongside outputs rather than inserting them into the image prompt. In ChatGPT/Work return actual generated image objects/downloads and accessible prompt/receipt artifacts, not bare local paths. Report conflicting or inaccessible requirements explicitly.

Static ads only. No video generation, product-URL research, campaign comparison harness, or changes to existing skill routing.
