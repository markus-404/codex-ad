# SKU Gallery Library

Use this reference when a marketer asks for a production prompt library, SKU-level prompt set, Shopee gallery, marketplace gallery, product detail page gallery, or a 4-6 image prompt batch.

## Library Shape

Create one prompt record per gallery image. A normal SKU library has 4-6 prompt records in display order:

1. Hero packshot with the primary claim.
2. Benefit or ingredient visual.
3. Texture, usage, or product-in-hand proof.
4. Social proof, offer, bundle, or comparison.
5. Lifestyle context or scenario fit.
6. Optional detail, routine, variant, or promotion slot.

Each prompt record contains these fields:

```yaml
sku: ""
slot_number: 1
slot purpose: "Hero product image"
platform_preset: "square-retargeting"
objective: "Marketplace conversion"
visual: ""
layout: ""
copy:
  headline: ""
  subline: ""
  offer: ""
negative prompt additions:
  - ""
reference image order:
  - "#0 logo"
  - "#1 product packshot"
readiness score: null
output QA notes: []
refinement instruction: ""
```

## Readiness Gate

Compile each record into prompt JSON with `scripts/compile_prompt.py`, then score every compiled prompt with `scripts/score_prompt.py` before generation. A production library is not ready until every prompt scores 75 or higher.

If a prompt scores below 75, revise the prompt record first. Do not compensate by asking the generator to "make it better" in broad language.

## Shopee Gallery Rules

- Keep every text string short enough to read on mobile.
- Use one main claim per image.
- Keep product packaging visible and large enough to identify.
- Repeat logo and product reference order consistently across all slots.
- Keep layout rhythm consistent across the SKU while varying the visual idea.
- Avoid medical, cure, miracle, guaranteed-result, or before/after claims unless the supplied brand/product context explicitly permits the exact wording.
- Preserve brand tone from the context files; do not turn premium beauty into cheap promo language.

## Batch Output

Return the prompt library as a list in gallery order. For each slot, include the prompt JSON or path, negative prompt, reference image order, readiness score, risks, recommendations, output QA notes, and refinement instruction.
