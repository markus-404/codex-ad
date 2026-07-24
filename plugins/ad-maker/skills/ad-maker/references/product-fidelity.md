# Product Fidelity

Use real product PNG compositing when the product must remain exact.

Prompt safeguards:
- Identify product reference images by uploaded index.
- State that product shape, label geometry, cap shape, package proportions, and visible material must remain unchanged.
- Include product drift restrictions in the negative prompt.

Compositing guidance:
- Generate the background and layout with reserved product space.
- Place the real product PNG over the generated background.
- Keep the product layer above the generated image.
- Use manual x, y, and width values in V1.

V1 does not include automated fidelity scoring.
