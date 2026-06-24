# Crafting Kit

Crafting Kit is an experimental game-development project focused on reusable crafting, gathering, progression, and item-production systems.

The goal is not to build a single game mechanic in isolation. The goal is to create a collection of modular systems that can be reused across browser RPGs, idle games, survival projects, management games, and future engine work.

## Project Vision

Many games include crafting, but most implementations are tightly coupled to a specific project.

Crafting Kit explores a more reusable approach:

- Recipes
- Materials
- Resource gathering
- Production chains
- Item quality
- Unlock requirements
- Progression gates
- Profession systems
- Economic balancing
- Crafting user interfaces

The long-term objective is to create systems that can be studied, copied, and adapted without needing to rebuild the same foundations repeatedly.

## Current Status

Early-stage project.

This repository is currently being used to define architecture, system boundaries, documentation, and future implementation goals.

The first working tool is a read-only Python validator for Crafting Kit content packs.

## Quick Start

Validate the starter content example:

```bash
python tools/validate_crafting_content.py examples/starter-content.json
```

Expected result:

```text
Crafting content is valid.
```

The validator checks item IDs, recipe inputs and outputs, profession references, resource node outputs, positive quantities, tag lists, and other basic schema rules.

## Planned Features

### Core Crafting

- Recipe definitions
- Material requirements
- Craft validation
- Item generation
- Success and failure rules
- Batch crafting support

### Gathering Systems

- Resource nodes
- Harvesting actions
- Tool requirements
- Resource rarity
- Gathering progression

### Profession Systems

- Blacksmithing
- Alchemy
- Cooking
- Tailoring
- Mining
- Woodcutting

Additional professions may be added later as the framework matures.

## Design Principles

- Reusable before game-specific.
- Simple before complex.
- Data-driven where possible.
- Easy to read and modify.
- Suitable for browser-based projects.
- Compatible with future engine experimentation.

## Relationship To Other Projects

Crafting Kit is intended to complement other repositories in this portfolio.

- DungeonDex explores RPG progression and gameplay systems.
- Depth Engine explores reusable browser RPG foundations.
- Crafting Kit focuses specifically on crafting and production mechanics that could eventually be integrated into larger projects.

## Long-Term Goal

Build a practical, reusable crafting framework that can serve as a foundation for future RPGs, management games, survival games, and experimentation projects without requiring the crafting system to be reinvented each time.
