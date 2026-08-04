# Refinement Workflows

## Reuse Prompt

Reuse the previous prompt exactly, changing only explicitly requested settings such as ratio, count, or model.

## Reuse Ad Brief

Reuse brand, product, objective, persona, scenario, and lineage metadata while allowing a new six-slot prompt.

## Vary

Supported axes:
- style
- layout
- scenario
- persona
- subtle
- strong

## Text Edit

Replace only requested copy strings. Preserve brand, product, visual direction, and layout unless the user asks for layout changes.

## Inpaint

Create an edit prompt scoped to the masked region. Preserve unmasked image areas.

## Post-Generation QA

After image generation, inspect the selected outputs before approval or bulk reuse. Record pass/fail notes by image and create one refinement instruction per failed item.

QA categories:

- Packaging fidelity: product shape, label geometry, cap shape, package proportions, color, and visible material match the supplied product reference.
- Mobile text readability: every rendered text string is short, legible, spelled correctly, and readable at marketplace thumbnail size.
- Platform layout consistency: ratio, safe zones, product scale, logo placement, and gallery rhythm match the chosen platform or Shopee gallery system.
- Claim risk: copy avoids unsupported cure, miracle, guaranteed-result, medical, or exaggerated claims.
- Brand tone: image, copy, typography, color, and offer framing match the supplied brand context.

Refinement instruction format:

```text
Refine image [slot/file]: fix [specific failed QA item]. Preserve [product/logo/background areas that passed]. Keep copy exactly "[approved text]" unless the failed item is text readability.
```
