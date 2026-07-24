# Prompt Template

Every generated prompt must use this exact slot order:

```text
- Visual:
- Color:
- Layout:
- Text:
- Fonts:
- Logo:
```

Rules:
- Target a maximum of 4000 characters.
- Address reference images by ordered index, starting at `uploaded logo #0` when a logo is provided.
- Quote every text string that should appear in the final ad.
- Repeat required copy once in `Layout` and once in `Text`.
- Use named fonts from brand guidelines.
- Use hex codes rather than color names when brand colors are known.
- Use quantified layout constraints when useful, such as `at least 12% of the canvas`.

Negative prompt must include:
- Do not use logos other than uploaded #0.
- Do not restyle, redraw, re-letter, or substitute the logo or wordmark.
- No garbled typography, distorted logo, or extraneous watermarks.
- No unrelated or competing product visuals.
- No invented wordmark next to the logo.
- Do not alter product shape, label geometry, cap shape, package proportions, or visible product materials.
