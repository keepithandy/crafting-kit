# Crafting Data Model Specification

This document defines the first reusable data model for Crafting Kit.

The goal is to describe crafting content in a way that is readable, portable, and not tied to one specific game theme.

## Model Goals

The data model should support:

- Reusable item definitions.
- Material and component requirements.
- Recipe inputs and outputs.
- Resource nodes for gathering.
- Profession and unlock metadata.
- Future balancing notes.
- Versioned content files.

This specification is intentionally framework-level. It defines the shape of the content before the project commits to a final UI or game loop.

## Content Pack Shape

A Crafting Kit content pack should eventually be able to describe all crafting content in one organized object.

```js
const craftingContent = {
  version: 1,
  items: {},
  recipes: {},
  resourceNodes: {},
  professions: {},
};
```

## Items

Items represent materials, tools, crafted goods, and future equipment.

```js
const item = {
  id: "iron_ore",
  name: "Iron Ore",
  type: "material",
  stackable: true,
  maxStack: 99,
  rarity: "common",
  value: 3,
  tags: ["ore", "metal", "blacksmithing"],
  description: "A chunk of raw iron ore.",
};
```

### Required Item Fields

- `id`: Stable machine-readable key.
- `name`: Player-facing display name.
- `type`: Item category such as `material`, `component`, `tool`, `consumable`, or `crafted`.

### Optional Item Fields

- `stackable`: Whether multiple copies can occupy one stack.
- `maxStack`: Maximum stack size.
- `rarity`: Commonness label.
- `value`: Base value for future economy balancing.
- `tags`: Search, filtering, and recipe grouping metadata.
- `description`: Player-facing description.

## Recipes

Recipes define how inputs become outputs.

```js
const recipe = {
  id: "iron_ingot_from_ore",
  name: "Smelt Iron Ingot",
  profession: "blacksmithing",
  levelRequired: 1,
  inputs: [
    { itemId: "iron_ore", quantity: 3 },
    { itemId: "coal", quantity: 1 }
  ],
  outputs: [
    { itemId: "iron_ingot", quantity: 1 }
  ],
  craftTimeSeconds: 5,
  tags: ["smelting", "metal"],
};
```

### Required Recipe Fields

- `id`: Stable machine-readable key.
- `name`: Player-facing display name.
- `inputs`: List of required materials.
- `outputs`: List of produced items.

### Optional Recipe Fields

- `profession`: Profession linked to the recipe.
- `levelRequired`: Minimum profession level.
- `craftTimeSeconds`: Future timing or queue metadata.
- `tags`: Grouping and search metadata.

## Recipe Inputs And Outputs

Inputs and outputs should use the same basic shape.

```js
const stackRequirement = {
  itemId: "iron_ore",
  quantity: 3,
};
```

### Required Stack Fields

- `itemId`: Item key from the item table.
- `quantity`: Positive whole number.

## Resource Nodes

Resource nodes describe gatherable sources such as ore veins, trees, herb patches, salvage piles, or monster drops.

```js
const resourceNode = {
  id: "starter_iron_vein",
  name: "Starter Iron Vein",
  type: "mining",
  levelRequired: 1,
  toolRequired: "pickaxe_basic",
  outputs: [
    { itemId: "iron_ore", quantityMin: 1, quantityMax: 3, weight: 80 },
    { itemId: "coal", quantityMin: 1, quantityMax: 1, weight: 20 }
  ],
  tags: ["ore", "starter", "blacksmithing"],
};
```

### Required Resource Node Fields

- `id`: Stable machine-readable key.
- `name`: Player-facing display name.
- `type`: Gathering category.
- `outputs`: Possible resource results.

### Optional Resource Node Fields

- `levelRequired`: Minimum gathering or profession level.
- `toolRequired`: Tool item key.
- `tags`: Grouping and search metadata.

## Resource Outputs

Resource outputs support quantity ranges and future weighted rolls.

```js
const resourceOutput = {
  itemId: "iron_ore",
  quantityMin: 1,
  quantityMax: 3,
  weight: 80,
};
```

### Required Resource Output Fields

- `itemId`: Item key from the item table.
- `quantityMin`: Minimum amount gained.
- `quantityMax`: Maximum amount gained.

### Optional Resource Output Fields

- `weight`: Relative chance weight for future random output selection.

## Professions

Professions describe skill tracks for crafting or gathering.

```js
const profession = {
  id: "blacksmithing",
  name: "Blacksmithing",
  type: "crafting",
  maxLevel: 100,
  description: "Craft metal bars, weapons, armor, and tools.",
};
```

### Required Profession Fields

- `id`: Stable machine-readable key.
- `name`: Player-facing display name.
- `type`: Profession category such as `crafting` or `gathering`.

### Optional Profession Fields

- `maxLevel`: Maximum planned level.
- `description`: Player-facing description.

## Unlock Requirements

Unlock requirements should stay generic so they can apply to recipes, nodes, professions, or future UI sections.

```js
const unlockRequirement = {
  profession: "blacksmithing",
  level: 5,
  requiredRecipeIds: ["iron_ingot_from_ore"],
  requiredItemIds: ["hammer_basic"],
};
```

All unlock fields are optional because different projects may gate content in different ways.

## Validation Rules

Early validation should check:

- Every item has a stable `id` and `name`.
- Every recipe input references a known item.
- Every recipe output references a known item.
- Every quantity is a positive whole number.
- Every resource node output references a known item.
- Every profession reference points to a known profession.
- Optional fields should fail safely when missing.

## Future Notes

This specification does not implement crafting behavior yet.

Next useful steps:

1. Add sample content using this schema.
2. Add read-only validation helpers.
3. Add a small mock crafting loop.
4. Add a simple browser UI after the data model stabilizes.
