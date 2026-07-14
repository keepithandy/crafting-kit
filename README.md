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

Working helpers and artifacts now include:

- A read-only Python validator for Crafting Kit content packs.
- A read-only crafting dry-run helper that previews recipe requirements and results without mutating inventory.
- A read-only gathering dry-run helper that previews resource-node gates and output tables without mutating inventory.
- Expanded starter content with multiple recipes, professions, and resource-node examples.
- A browser-only crafting interface prototype for recipe selection, mock inventory display, craftable/blocked states, and result preview.
- Documentation for resource gathering, profession progression, and first-pass economic balance.

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

Run the dry-run helper from Python:

```python
import json
from pathlib import Path

from tools.crafting_dry_run import crafting_dry_run
from tools.gathering_dry_run import gathering_dry_run

content = json.loads(Path("examples/starter-content.json").read_text(encoding="utf-8"))

craftable = crafting_dry_run(content, "iron_ingot_from_ore", {"iron_ore": 3, "coal": 1})
blocked = crafting_dry_run(content, "iron_ingot_from_ore", {"iron_ore": 1, "coal": 0})

harvest_preview = gathering_dry_run(
    content,
    "starter_iron_vein",
    actor={"levels": {"mining": 1}},
    inventory={"pickaxe_basic": 1},
)
```

Run the dry-run tests:

```bash
python -m unittest discover -s tests
```

Open the browser prototype directly:

```text
prototype/crafting-interface.html
```

## Current Architecture Docs

- `docs/resource-gathering-framework.md`
- `docs/profession-progression-architecture.md`
- `docs/economic-balance-layer.md`

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
