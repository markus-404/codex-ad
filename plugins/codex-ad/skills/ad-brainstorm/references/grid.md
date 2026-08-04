# The 10x10 Grid

10 format archetypes x 10 angle pivots = 100 cells. Exactly one concept per cell.

Format is *how the ad is shot*. Angle is *what it argues*. Keep them independent —
when a UGC monologue and a founder story end up making the same argument in the
same voice, the axes have collapsed and `hook_distinctness` will show it.

## 10 Format Archetypes (rows, F1-F10)

| # | Format | Description |
|---|---|---|
| 1 | UGC monologue | Selfie cam, first-person, raw — one creator talking to camera |
| 2 | Before/after timer | Visible time stamp framing a transformation beat |
| 3 | Founder story | POV from the product creator on why it exists |
| 4 | Parody news | Fake broadcast segment — anchor + field cut |
| 5 | Reddit reaction | Screenshot of a Reddit post + reaction face or voiceover |
| 6 | Listicle | Numbered reasons, comparison, or top-X format |
| 7 | Expert breakdown | Authority figure walks through the mechanism |
| 8 | Day-in-the-life | Lifestyle vlog with the product embedded naturally |
| 9 | Testimonial cut | Rapid-fire real customer quotes, minimally edited |
| 10 | ASMR product moment | Sensory close-up with ambient sound, no voiceover |

## 10 Angle Pivots (columns, A1-A10)

| # | Angle | The Frame |
|---|---|---|
| 1 | Pain killer | Removes a specific sharp pain the viewer already has |
| 2 | Status symbol | Signals who you are to others — identity projection |
| 3 | Time saver | Gives hours back — efficiency and simplification |
| 4 | Money saver | Costs less over time than the alternatives |
| 5 | Identity badge | Aligns with a tribe, community, or self-concept |
| 6 | Secret weapon | Insider edge nobody else knows about yet |
| 7 | Category disruptor | Rejects how everyone else in the category does this |
| 8 | Peer recommendation | Friend-told-me framing — warm social proof |
| 9 | Expert endorsement | Authority figure (derm, coach, engineer) co-signs |
| 10 | Contrarian truth | The uncomfortable fact the category hides from you |

## Platform values

`Meta feed`, `Meta Reels`, `TikTok`, `YouTube Shorts`, `YouTube long-form`,
`Reddit`, `LinkedIn`, `Pinterest`. Exact strings — the validator matches them literally.

## Modifiers

- **`Skip formats [X, Y]`** — drop those rows from `grid.formats`. The expected cell
  count shrinks with the grid; the validator derives it from the arrays, never from
  a hard-coded 100.
- **`Focus on [Meta / TikTok / YouTube]`** — bias `platform` toward that family. Do not
  collapse to a single value; `platform_spread` scores diversity, and a
  platform-locked run will score low by design.
- **`Target [audience]`** — override the scraped ICP in the audience map.
- **`Generate in [language]`** — hooks and summaries in the target language. Grid axis
  names, `platform` values, and all JSON keys stay in English so validation still works.
