"""Preview Crafting Kit recipe craftability without mutating inventory.

This helper loads a Crafting Kit content pack, selects a recipe, and checks a
simple inventory map to determine whether the recipe can be crafted.

Usage:
    python tools/crafting_preview.py examples/starter-content.json iron_ingot_from_ore --inventory iron_ore=3 coal=1

Exit codes:
    0 = recipe can be crafted
    1 = recipe cannot be crafted
    2 = content, recipe, or inventory input could not be loaded
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from validate_crafting_content import validate_content


Inventory = dict[str, int]


def is_positive_int(value: Any) -> bool:
    """Return True when value is a positive whole number."""
    return isinstance(value, int) and value > 0


def load_json_file(path: Path) -> Any:
    """Load JSON from disk."""
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def parse_inventory(entries: list[str]) -> Inventory:
    """Parse command-line inventory entries like item_id=quantity."""
    inventory: Inventory = {}

    for entry in entries:
        if "=" not in entry:
            raise ValueError(f"Inventory entry '{entry}' must use item_id=quantity format.")

        item_id, raw_quantity = entry.split("=", 1)
        item_id = item_id.strip()
        raw_quantity = raw_quantity.strip()

        if not item_id:
            raise ValueError("Inventory item id cannot be empty.")

        try:
            quantity = int(raw_quantity)
        except ValueError as error:
            raise ValueError(f"Inventory quantity for '{item_id}' must be an integer.") from error

        if quantity < 0:
            raise ValueError(f"Inventory quantity for '{item_id}' cannot be negative.")

        inventory[item_id] = inventory.get(item_id, 0) + quantity

    return inventory


def get_recipe(content: dict[str, Any], recipe_id: str) -> dict[str, Any] | None:
    """Return a recipe by ID from a validated content pack."""
    recipes = content.get("recipes", {})
    recipe = recipes.get(recipe_id)
    return recipe if isinstance(recipe, dict) else None


def craft_preview(recipe: dict[str, Any], inventory: Inventory) -> dict[str, Any]:
    """Return read-only craftability details for a recipe and inventory."""
    missing: list[dict[str, Any]] = []

    for requirement in recipe.get("inputs", []):
        item_id = requirement["itemId"]
        required = requirement["quantity"]
        available = inventory.get(item_id, 0)

        if available < required:
            missing.append(
                {
                    "itemId": item_id,
                    "required": required,
                    "available": available,
                    "missing": required - available,
                }
            )

    return {
        "recipeId": recipe["id"],
        "recipeName": recipe["name"],
        "canCraft": not missing,
        "missing": missing,
        "outputs": recipe.get("outputs", []),
    }


def print_preview(preview: dict[str, Any]) -> None:
    """Print a human-readable crafting preview."""
    print(f"Recipe: {preview['recipeName']} ({preview['recipeId']})")

    if preview["canCraft"]:
        print("Status: craftable")
        print("Outputs:")
        for output in preview["outputs"]:
            print(f"- {output['itemId']} x{output['quantity']}")
        return

    print("Status: blocked")
    print("Missing materials:")
    for missing in preview["missing"]:
        print(
            f"- {missing['itemId']}: needs {missing['required']}, "
            f"has {missing['available']}, missing {missing['missing']}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Preview whether a Crafting Kit recipe can be crafted.")
    parser.add_argument("content_path", type=Path, help="Path to a Crafting Kit JSON content file.")
    parser.add_argument("recipe_id", help="Recipe ID to preview.")
    parser.add_argument(
        "--inventory",
        nargs="*",
        default=[],
        help="Inventory entries in item_id=quantity format.",
    )
    args = parser.parse_args()

    try:
        content = load_json_file(args.content_path)
    except OSError as error:
        print(f"Could not read file: {error}")
        return 2
    except json.JSONDecodeError as error:
        print(f"Could not parse JSON: {error}")
        return 2

    errors = validate_content(content)
    if errors:
        print("Content pack is invalid:")
        for error in errors:
            print(f"- {error}")
        return 2

    try:
        inventory = parse_inventory(args.inventory)
    except ValueError as error:
        print(f"Invalid inventory: {error}")
        return 2

    recipe = get_recipe(content, args.recipe_id)
    if recipe is None:
        print(f"Unknown recipe: {args.recipe_id}")
        return 2

    preview = craft_preview(recipe, inventory)
    print_preview(preview)

    return 0 if preview["canCraft"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
