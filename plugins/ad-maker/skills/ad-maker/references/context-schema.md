# Context Schema

## Brand

Required fields:
- `name`
- `website`
- `vertical`
- `description`
- `unique_value_propositions`
- `target_audience`
- `category`
- `category_needs`
- `notes`
- `guidelines.logos`
- `guidelines.colors`
- `guidelines.fonts.headline`
- `guidelines.fonts.body`
- `guidelines.tone`
- `guidelines.preferred_words`
- `guidelines.avoid_words`

## Product

Required fields:
- `name`
- `url`
- `categories`
- `description`
- `unique_selling_points`
- `images`
- `related_scenarios`
- `related_personas`
- `awareness_level`
- `market_sophistication`

Allowed `awareness_level` values:
- `L1 Unaware`
- `L2 Problem aware`
- `L3 Solution aware`
- `L4 Product/brand aware`
- `L5 Most aware`

Allowed `market_sophistication` values:
- `L1`
- `L2`
- `L3`
- `L4`
- `L5`

## Persona

Required fields:
- `name`
- `summary`
- `core_motivations`
- `barriers_objections`
- `what_convinces`
- `preferred_channels`

## Scenario

Required fields:
- `name`
- `scene`
- `trigger`
- `pain_points`
- `desired_outcome`
- `emotional_state`
- `current_alternatives`
- `barrier`
