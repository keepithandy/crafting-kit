# Economic Balance Layer

## Goal

Create a first-pass balance framework for crafting costs, resource flow, and item value without building a full economy simulator.

## Balance assumptions

Starter content uses a rough value model:

- Raw common materials have low value.
- Crafted components should usually be worth more than one raw input.
- Finished items should not create infinite profit loops from cheap recipes.
- Tool recipes can cost more because they unlock gathering access.
- Consumables should be valuable enough to matter but not dominate progression.

## Starter value examples

| Recipe | Input value | Output value | Notes |
| --- | ---: | ---: | --- |
| Smelt Iron Ingot | 11 | 10 | Slight value loss; smelting is a conversion step, not a profit printer |
| Brew Healing Potion | 5 | 8 | Modest value gain; useful consumable output |
| Stitch Simple Cloak | 6 | 7 | Small value gain; starter equipment |
| Forge Basic Pickaxe | 21 | 15 | Value loss; pickaxe is utility/tool access, not resale profit |

## Infinite-profit risk checks

A recipe is risky if:

- Output value is far above input value and inputs are easy to gather.
- The output can be recycled into more inputs than it consumed.
- A tool unlocks the same resources needed to craft itself with no friction.
- Batch crafting multiplies profit without time, durability, or scarcity cost.

## Recommended starter rules

1. Document input and output values before adding automation.
2. Keep starter recipes near break-even.
3. Let consumables have small positive value gains.
4. Let tools and unlock items have value losses because they provide access.
5. Do not add vendor resale loops until balancing is more mature.
6. Treat resource rarity and craft time as balance levers later.

## Future fields

Possible future recipe fields:

```json
{
  "xpReward": 5,
  "stationRequired": "forge",
  "batchSize": 1,
  "economyNotes": "Utility unlock, not profit recipe."
}
```

Possible future resource-node fields:

```json
{
  "cooldownSeconds": 60,
  "durabilityCost": 1,
  "rareOutputChance": 0.05
}
```

## Current decision

The current layer remains documentation-first. The starter content includes item values and recipe examples, but no economy simulation is required yet.
