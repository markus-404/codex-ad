# Scoring Rubric

Score prompt JSON before image generation when the user asks for a quality
check, a recommendation, or multiple concepts. For production, gallery,
Shopee, or multi-prompt SKU batches, scoring is mandatory before generation.

Each category is scored from 0 to 10:

- Hook clarity: the first-glance idea is specific and visual.
- Product prominence: the product is visible, referenced, and given canvas space.
- Offer clarity: the offer or CTA is quoted and placed near the focal path.
- Audience fit: the persona, pain point, or desired outcome is present.
- Brand consistency: colors, fonts, logo handling, and tone are present.
- Platform fit: ratio and layout match the selected platform preset.
- Text-render risk: required text is short, quoted, and repeated in Layout/Text.
- Product-fidelity risk: product drift is restricted and product references exist.
- Novelty: the visual is specific enough to avoid generic product-on-background output.

Use `scripts/score_prompt.py` for deterministic scoring. Scores below 75 need a
revision before image generation.
