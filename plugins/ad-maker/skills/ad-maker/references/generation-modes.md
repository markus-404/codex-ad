# Generation Modes

## Clone

Use when the user provides a reference ad and wants to adapt the layout or concept to their brand and product.

Required inputs:
- reference ad image or description
- brand context
- product context

Output:
- visual analysis of the reference ad
- six-slot prompt for the adapted ad
- negative prompt
- ordered image reference list
- metadata with mode `clone`

## Iterate

Use when the user provides an existing winning ad and wants new variants.

Required inputs:
- original ad image or description
- performance notes when available
- brand context
- product context

Output:
- original ad analysis
- 3 strategies
- 12 named ad ideas
- six-slot prompt per selected ad idea
- metadata with mode `iterate`

## Natural-language brief

Use when the user gives a natural-language static ad request.

Required inputs:
- natural-language request
- brand context
- product context

Output:
- interpreted brief
- six-slot prompt
- negative prompt
- ordered image reference list
- metadata with mode `brief`
