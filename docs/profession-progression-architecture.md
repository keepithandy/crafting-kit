# Profession Progression Architecture

## Goal

Define a small profession model that can support crafting and gathering progression without forcing every future profession into the first implementation.

## Profession record

Each profession should have:

- `id`: stable key.
- `name`: display name.
- `type`: either `crafting` or `gathering`.
- `maxLevel`: maximum reachable level.
- `description`: short player-facing explanation.

Optional future fields:

- `xpCurve`: named curve such as `linear`, `slow`, or `milestone`.
- `unlockConditions`: requirements for unlocking the profession.
- `specializations`: sub-paths such as Weapon Smithing or Potion Brewing.
- `tags`: grouping labels for UI and filtering.

## Starter professions

| Profession | Type | First use |
| --- | --- | --- |
| Blacksmithing | Crafting | Smelting ingots and forging starter tools |
| Mining | Gathering | Harvesting ore and coal |
| Alchemy | Crafting | Brewing starter potions |
| Tailoring | Crafting | Creating cloth equipment |
| Herbalism | Gathering | Gathering herbs and reagents |

## XP model

The recommended early model is deliberately simple:

- A successful craft or harvest can award profession XP later.
- Failed or blocked dry-runs should not award XP.
- XP values should live on recipes or resource nodes only after balance rules are clearer.
- Level requirements should gate recipes and nodes before a full XP curve exists.

## Unlock model

Early unlocks should be data-driven and readable:

```json
{
  "profession": "alchemy",
  "levelRequired": 1
}
```

Future unlocks can add:

- Required items.
- Required completed recipes.
- Required gathered resources.
- Required account/profile milestones.
- Required zone or station access.

## Implementation guardrails

- Keep progression data separate from UI rendering.
- Avoid hard-coded profession behavior in helpers.
- Keep dry-run helpers read-only.
- Do not add live balancing until the economic layer is clearer.
- Support a small starter set first; do not require every profession to be complete.
