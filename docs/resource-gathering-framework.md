# Resource Gathering Framework

## Goal

Define the first reusable gathering foundation for Crafting Kit without requiring a full crafting UI, backend, persistence layer, or live economy simulation.

## Core objects

### Resource node

A resource node represents something the player can harvest, mine, scavenge, chop, or gather.

Required fields:

- `id`: stable machine-readable key.
- `name`: player-readable label.
- `type`: gathering category such as `mining`, `herbalism`, `woodcutting`, `scavenging`, or `monster_part`.
- `levelRequired`: minimum profession level.
- `outputs`: weighted item-output table.

Optional fields:

- `toolRequired`: item ID required to harvest the node.
- `tags`: searchable grouping labels.
- `description`: player-facing explanation.

### Output rule

Each output rule describes a possible item result.

Required fields:

- `itemId`: item produced by the node.
- `quantityMin`: lowest quantity returned.
- `quantityMax`: highest quantity returned.
- `weight`: relative selection weight.

Rules:

- `quantityMin` and `quantityMax` must be positive integers.
- `quantityMin` cannot exceed `quantityMax`.
- Output weights are relative, not percentages.
- Nodes may produce one or multiple output rows.
- A dry-run preview should be deterministic and read-only.

## Starter node examples

The starter content includes three node types:

| Node | Type | Primary outputs | Tool gate |
| --- | --- | --- | --- |
| Starter Iron Vein | `mining` | Iron Ore, Coal | Basic Pickaxe |
| Wild Herb Patch | `herbalism` | Wild Herb, Water Vial | None |
| Abandoned Supply Crate | `scavenging` | Cloth Scrap, Thread | None |

## Harvest action model

A harvest action should eventually check:

1. The node exists.
2. The actor has the required profession level.
3. The required tool is present when `toolRequired` is set.
4. The node outputs reference known item IDs.
5. The result can be previewed without mutating inventory.

## Current helper

`tools/gathering_dry_run.py` provides a read-only preview helper. It checks level and tool gates and returns the node output table as a deterministic preview.

## Future extension points

- Tool durability.
- Profession XP rewards.
- Node cooldowns.
- Rare output modifiers.
- Biome or zone restrictions.
- Party/worker gathering assignments.
- Monster-part gathering after combat.
