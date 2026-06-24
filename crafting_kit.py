"""Crafting Kit core recipe helpers.

This module is the first small Python foundation for Crafting Kit. It keeps the
logic dependency-free and data-driven so the same concepts can later move into a
browser UI, game engine, or content pipeline.

The current focus is Issue #1: Core Recipe System Foundation.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any


ItemTable = dict[str, dict[str, Any]]
RecipeTable = dict[str, dict[str, Any]]
Inventory = dict[str, int]


@dataclass(frozen=True)
class ValidationResult:
    """Result object returned by validation helpers."""

    ok: bool
    errors: tuple[str, ...]


def is_positive_int(value: Any) -> bool:
    """Return True when value is a positive whole number."""

    return isinstance(value, int) and value > 0


def get_inventory_quantity(inventory: Inventory, item_id: str) -> int:
    """Return a safe non-negative inventory quantity.

    Malformed, missing, or negative values are treated as zero so recipe checks
    fail safely instead of raising type errors.
    """

    quantity = inventory.get(item_id, 0)

    if not isinstance(quantity, int) or quantity < 0:
        return 0

    return quantity


def validate_items(items: Any) -> ValidationResult:
    """Validate the item table used by recipes and inventories."""

    errors: list[str] = []

    if not isinstance(items, dict):
        return ValidationResult(False, ("items must be a dictionary",))

    for item_id, item in items.items():
        if not isinstance(item_id, str) or not item_id:
            errors.append("item keys must be non-empty strings")
            continue

        if not isinstance(item, dict):
            errors.append(f"item '{item_id}' must be a dictionary")
            continue

        if item.get("id") != item_id:
            errors.append(f"item '{item_id}' must include matching id")

        if not isinstance(item.get("name"), str) or not item.get("name"):
            errors.append(f"item '{item_id}' must include a non-empty name")

        if not isinstance(item.get("type"), str) or not item.get("type"):
            errors.append(f"item '{item_id}' must include a non-empty type")

        if "maxStack" in item and not is_positive_int(item["maxStack"]):
            errors.append(f"item '{item_id}' maxStack must be a positive integer")

        if "value" in item and not isinstance(item["value"], (int, float)):
            errors.append(f"item '{item_id}' value must be numeric")

        if "tags" in item and not isinstance(item["tags"], list):
            errors.append(f"item '{item_id}' tags must be a list")

    return ValidationResult(not errors, tuple(errors))


def validate_stack_list(stacks: Any, items: ItemTable, owner: str) -> list[str]:
    """Validate recipe input/output stack lists."""

    errors: list[str] = []

    if not isinstance(stacks, list) or not stacks:
        return [f"{owner} must be a non-empty list"]

    for index, stack in enumerate(stacks):
        label = f"{owner}[{index}]"

        if not isinstance(stack, dict):
            errors.append(f"{label} must be a dictionary")
            continue

        item_id = stack.get("itemId")
        quantity = stack.get("quantity")

        if not isinstance(item_id, str) or not item_id:
            errors.append(f"{label} must include a non-empty itemId")
        elif item_id not in items:
            errors.append(f"{label} references unknown item '{item_id}'")

        if not is_positive_int(quantity):
            errors.append(f"{label} quantity must be a positive integer")

    return errors


def validate_recipes(recipes: Any, items: ItemTable) -> ValidationResult:
    """Validate recipe definitions against an item table."""

    errors: list[str] = []

    item_result = validate_items(items)
    errors.extend(item_result.errors)

    if not isinstance(recipes, dict):
        errors.append("recipes must be a dictionary")
        return ValidationResult(False, tuple(errors))

    for recipe_id, recipe in recipes.items():
        if not isinstance(recipe_id, str) or not recipe_id:
            errors.append("recipe keys must be non-empty strings")
            continue

        if not isinstance(recipe, dict):
            errors.append(f"recipe '{recipe_id}' must be a dictionary")
            continue

        if recipe.get("id") != recipe_id:
            errors.append(f"recipe '{recipe_id}' must include matching id")

        if not isinstance(recipe.get("name"), str) or not recipe.get("name"):
            errors.append(f"recipe '{recipe_id}' must include a non-empty name")

        errors.extend(validate_stack_list(recipe.get("inputs"), items, f"recipe '{recipe_id}' inputs"))
        errors.extend(validate_stack_list(recipe.get("outputs"), items, f"recipe '{recipe_id}' outputs"))

        if "levelRequired" in recipe and not is_positive_int(recipe["levelRequired"]):
            errors.append(f"recipe '{recipe_id}' levelRequired must be a positive integer")

        if "craftTimeSeconds" in recipe and not is_positive_int(recipe["craftTimeSeconds"]):
            errors.append(f"recipe '{recipe_id}' craftTimeSeconds must be a positive integer")

    return ValidationResult(not errors, tuple(errors))


def can_craft(recipe: dict[str, Any], inventory: Inventory) -> bool:
    """Return True when inventory contains enough materials for a recipe."""

    if not isinstance(recipe, dict) or not isinstance(inventory, dict):
        return False

    inputs = recipe.get("inputs")
    if not isinstance(inputs, list):
        return False

    for stack in inputs:
        if not isinstance(stack, dict):
            return False

        item_id = stack.get("itemId")
        quantity = stack.get("quantity")

        if not isinstance(item_id, str) or not is_positive_int(quantity):
            return False

        if get_inventory_quantity(inventory, item_id) < quantity:
            return False

    return True


def craft(recipe: dict[str, Any], inventory: Inventory) -> Inventory:
    """Return a new inventory after crafting one recipe.

    The input inventory is never mutated. A ValueError is raised when the recipe
    cannot be crafted from the supplied inventory.
    """

    if not can_craft(recipe, inventory):
        raise ValueError("inventory does not contain the required recipe inputs")

    next_inventory = deepcopy(inventory)

    for stack in recipe["inputs"]:
        item_id = stack["itemId"]
        quantity = stack["quantity"]
        next_inventory[item_id] = get_inventory_quantity(next_inventory, item_id) - quantity

        if next_inventory[item_id] <= 0:
            del next_inventory[item_id]

    for stack in recipe.get("outputs", []):
        item_id = stack["itemId"]
        quantity = stack["quantity"]
        next_inventory[item_id] = get_inventory_quantity(next_inventory, item_id) + quantity

    return next_inventory


SAMPLE_ITEMS: ItemTable = {
    "iron_ore": {
        "id": "iron_ore",
        "name": "Iron Ore",
        "type": "material",
        "stackable": True,
        "maxStack": 99,
        "rarity": "common",
        "value": 3,
        "tags": ["ore", "metal", "blacksmithing"],
    },
    "coal": {
        "id": "coal",
        "name": "Coal",
        "type": "material",
        "stackable": True,
        "maxStack": 99,
        "rarity": "common",
        "value": 2,
        "tags": ["fuel", "blacksmithing"],
    },
    "iron_ingot": {
        "id": "iron_ingot",
        "name": "Iron Ingot",
        "type": "component",
        "stackable": True,
        "maxStack": 99,
        "rarity": "common",
        "value": 12,
        "tags": ["bar", "metal", "blacksmithing"],
    },
}


SAMPLE_RECIPES: RecipeTable = {
    "iron_ingot_from_ore": {
        "id": "iron_ingot_from_ore",
        "name": "Smelt Iron Ingot",
        "inputs": [
            {"itemId": "iron_ore", "quantity": 3},
            {"itemId": "coal", "quantity": 1},
        ],
        "outputs": [
            {"itemId": "iron_ingot", "quantity": 1},
        ],
        "craftTimeSeconds": 5,
        "tags": ["smelting", "metal"],
    }
}


def run_demo() -> None:
    """Run a tiny command-line smoke demo."""

    result = validate_recipes(SAMPLE_RECIPES, SAMPLE_ITEMS)
    print(f"Recipe data valid: {result.ok}")

    if not result.ok:
        for error in result.errors:
            print(f"- {error}")
        return

    inventory = {"iron_ore": 6, "coal": 2}
    recipe = SAMPLE_RECIPES["iron_ingot_from_ore"]

    print(f"Starting inventory: {inventory}")
    print(f"Can craft {recipe['name']}: {can_craft(recipe, inventory)}")
    print(f"After craft: {craft(recipe, inventory)}")


if __name__ == "__main__":
    run_demo()
