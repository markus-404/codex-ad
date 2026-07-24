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

## Authoring the creative slots

`Visual` and `Layout` carry the creative idea. Write them yourself for every prompt. Never ship the fallback template wording for a real ad.

Write `Visual` as camera direction: who is in frame, what they are doing, time of day, lighting, setting, mood. Ground it in the scenario `scene` and the persona, then go beyond both.

Write `Layout` as spatial instruction: where the product sits, how much canvas it occupies, where each copy string is placed, and what the eye should hit first.

Vary both across a variant set. Twelve ad ideas must not share one composition described twelve times.

Pass authored slots to `scripts/compile_prompt.py` with `--visual` and `--layout`. When either is omitted the script falls back to a deterministic template that is correct in structure but generic in content, suitable for smoke tests and not for delivered ads.

`Color`, `Text`, `Fonts`, and `Logo` stay mechanical. They are compiled from brand guidelines and the exact copy strings, and must not be improvised.

## Rules

- Target a maximum of 4000 characters.
- Address reference images by ordered index, starting at `uploaded logo #0` when a logo is provided.
- Quote every text string that should appear in the final ad.
- Repeat required copy once in `Layout` and once in `Text`.
- Use named fonts from brand guidelines.
- Use hex codes rather than color names when brand colors are known.
- Use quantified layout constraints when useful, such as `at least 12% of the canvas`.

## Negative prompt

Negative prompt must include:
- Do not use logos other than uploaded #0.
- Do not restyle, redraw, re-letter, or substitute the logo or wordmark.
- No garbled typography, distorted logo, or extraneous watermarks.
- No unrelated or competing product visuals.
- No invented wordmark next to the logo.
- Do not alter product shape, label geometry, cap shape, package proportions, or visible product materials.
