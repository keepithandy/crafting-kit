"""Validate Crafting Kit content packs.

This is a read-only helper for checking early Crafting Kit data files.
It validates the framework-level schema described in docs/crafting-data-model.md.

Usage:
    python tools/validate_crafting_content.py examples/starter-content.json

Exit codes:
    0 = valid content
    1 = validation errors found
    2 = file could not be loaded
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


VALID_ITEM_TYPES = {"material", "component", "tool", "consumable", "crafted", "equipment"}
VALID_PROFESSION_TYPES = {"crafting", "gathering"}


def is_positive_int(value: Any) -> bool:
    """Return True when value is a positive whole number."""
    return isinstance(value, int) and value > 0


def is_non_empty_string(value: Any) -> bool:
    """Return True when value is a non-empty string."""
    return isinstance(value, str) and bool(value.strip())


def validate_tags(path: str, tags: Any, errors: list[str]) -> None:
    """Validate an optional list of non-empty tag strings."""
    if tags is None:
        return

    if not isinstance(tags, list):
        errors.append(f"{path}.tags must be a list when present.")
        return

    for index, tag in enumerate(tags):
        if not is_non_empty_string(tag):
            errors.append(f"{path}.tags[{index}] must be a non-empty string.")


def validate_id_map(section_name: str, value: Any, errors: list[str]) -> dict[str, Any]:
    """Validate that a top-level content section is an object map."""
    if value is None:
        return {}

    if not isinstance(value, dict):
        errors.append(f"{section_name} must be an object map.")
        return {}

    return value


def validate_items(items: dict[str, Any], errors: list[str]) -> set[str]:
    """Validate item records and return known item IDs."""
    known_item_ids: set[str] = set()

    for key, item in items.items():
        path = f"items.{key}"

        if not isinstance(item, dict):
            errors.append(f"{path} must be an object.")
            continue

        item_id = item.get("id")
        name = item.get("name")
        item_type = item.get("type")

        if not is_non_empty_string(item_id):
            errors.append(f"{path}.id must be a non-empty string.")
        elif item_id != key:
            errors.append(f"{path}.id must match its map key.")
        else:
            known_item_ids.add(item_id)

        if not is_non_empty_string(name):
            errors.append(f"{path}.name must be a non-empty string.")

        if not is_non_empty_string(item_type):
            errors.append(f"{path}.type must be a non-empty string.")
        elif item_type not in VALID_ITEM_TYPES:
            errors.append(
                f"{path}.type must be one of: {', '.join(sorted(VALID_ITEM_TYPES))}."
            )

        max_stack = item.get("maxStack")
        if max_stack is not None and not is_positive_int(max_stack):
            errors.append(f"{path}.maxStack must be a positive integer when present.")

        value = item.get("value")
        if value is not None and not isinstance(value, (int, float)):
            errors.append(f"{path}.value must be numeric when present.")

        validate_tags(path, item.get("tags"), errors)

    return known_item_ids


def validate_stack_list(
    path: str,
    stacks: Any,
    known_item_ids: set[str],
    errors: list[str],
) -> None:
    """Validate recipe input/output stacks."""
    if not isinstance(stacks, list) or not stacks:
        errors.append(f"{path} must be a non-empty list.")
        return

    for index, stack in enumerate(stacks):
        stack_path = f"{path}[{index}]"

        if not isinstance(stack, dict):
            errors.append(f"{stack_path} must be an object.")
            continue

        item_id = stack.get("itemId")
        quantity = stack.get("quantity")

        if not is_non_empty_string(item_id):
            errors.append(f"{stack_path}.itemId must be a non-empty string.")
        elif item_id not in known_item_ids:
            errors.append(f"{stack_path}.itemId references unknown item '{item_id}'.")

        if not is_positive_int(quantity):
            errors.append(f"{stack_path}.quantity must be a positive integer.")


def validate_professions(professions: dict[str, Any], errors: list[str]) -> set[str]:
    """Validate profession records and return known profession IDs."""
    known_profession_ids: set[str] = set()

    for key, profession in professions.items():
        path = f"professions.{key}"

        if not isinstance(profession, dict):
            errors.append(f"{path} must be an object.")
            continue

        profession_id = profession.get("id")
        name = profession.get("name")
        profession_type = profession.get("type")

        if not is_non_empty_string(profession_id):
            errors.append(f"{path}.id must be a non-empty string.")
        elif profession_id != key:
            errors.append(f"{path}.id must match its map key.")
        else:
            known_profession_ids.add(profession_id)

        if not is_non_empty_string(name):
            errors.append(f"{path}.name must be a non-empty string.")

        if not is_non_empty_string(profession_type):
            errors.append(f"{path}.type must be a non-empty string.")
        elif profession_type not in VALID_PROFESSION_TYPES:
            errors.append(
                f"{path}.type must be one of: {', '.join(sorted(VALID_PROFESSION_TYPES))}."
            )

        max_level = profession.get("maxLevel")
        if max_level is not None and not is_positive_int(max_level):
            errors.append(f"{path}.maxLevel must be a positive integer when present.")

        validate_tags(path, profession.get("tags"), errors)

    return known_profession_ids


def validate_recipes(
    recipes: dict[str, Any],
    known_item_ids: set[str],
    known_profession_ids: set[str],
    errors: list[str],
) -> None:
    """Validate recipe records."""
    for key, recipe in recipes.items():
        path = f"recipes.{key}"

        if not isinstance(recipe, dict):
            errors.append(f"{path} must be an object.")
            continue

        recipe_id = recipe.get("id")
        name = recipe.get("name")

        if not is_non_empty_string(recipe_id):
            errors.append(f"{path}.id must be a non-empty string.")
        elif recipe_id != key:
            errors.append(f"{path}.id must match its map key.")

        if not is_non_empty_string(name):
            errors.append(f"{path}.name must be a non-empty string.")

        validate_stack_list(f"{path}.inputs", recipe.get("inputs"), known_item_ids, errors)
        validate_stack_list(f"{path}.outputs", recipe.get("outputs"), known_item_ids, errors)

        profession = recipe.get("profession")
        if profession is not None:
            if not is_non_empty_string(profession):
                errors.append(f"{path}.profession must be a non-empty string when present.")
            elif profession not in known_profession_ids:
                errors.append(f"{path}.profession references unknown profession '{profession}'.")

        level_required = recipe.get("levelRequired")
        if level_required is not None and not is_positive_int(level_required):
            errors.append(f"{path}.levelRequired must be a positive integer when present.")

        craft_time = recipe.get("craftTimeSeconds")
        if craft_time is not None and not is_positive_int(craft_time):
            errors.append(f"{path}.craftTimeSeconds must be a positive integer when present.")

        validate_tags(path, recipe.get("tags"), errors)


def validate_resource_nodes(
    resource_nodes: dict[str, Any],
    known_item_ids: set[str],
    errors: list[str],
) -> None:
    """Validate resource node records."""
    for key, node in resource_nodes.items():
        path = f"resourceNodes.{key}"

        if not isinstance(node, dict):
            errors.append(f"{path} must be an object.")
            continue

        node_id = node.get("id")
        name = node.get("name")
        node_type = node.get("type")

        if not is_non_empty_string(node_id):
            errors.append(f"{path}.id must be a non-empty string.")
        elif node_id != key:
            errors.append(f"{path}.id must match its map key.")

        if not is_non_empty_string(name):
            errors.append(f"{path}.name must be a non-empty string.")

        if not is_non_empty_string(node_type):
            errors.append(f"{path}.type must be a non-empty string.")

        level_required = node.get("levelRequired")
        if level_required is not None and not is_positive_int(level_required):
            errors.append(f"{path}.levelRequired must be a positive integer when present.")

        tool_required = node.get("toolRequired")
        if tool_required is not None:
            if not is_non_empty_string(tool_required):
                errors.append(f"{path}.toolRequired must be a non-empty string when present.")
            elif tool_required not in known_item_ids:
                errors.append(f"{path}.toolRequired references unknown item '{tool_required}'.")

        outputs = node.get("outputs")
        if not isinstance(outputs, list) or not outputs:
            errors.append(f"{path}.outputs must be a non-empty list.")
        else:
            for index, output in enumerate(outputs):
                output_path = f"{path}.outputs[{index}]"

                if not isinstance(output, dict):
                    errors.append(f"{output_path} must be an object.")
                    continue

                item_id = output.get("itemId")
                quantity_min = output.get("quantityMin")
                quantity_max = output.get("quantityMax")
                weight = output.get("weight")

                if not is_non_empty_string(item_id):
                    errors.append(f"{output_path}.itemId must be a non-empty string.")
                elif item_id not in known_item_ids:
                    errors.append(f"{output_path}.itemId references unknown item '{item_id}'.")

                if not is_positive_int(quantity_min):
                    errors.append(f"{output_path}.quantityMin must be a positive integer.")

                if not is_positive_int(quantity_max):
                    errors.append(f"{output_path}.quantityMax must be a positive integer.")

                if (
                    is_positive_int(quantity_min)
                    and is_positive_int(quantity_max)
                    and quantity_min > quantity_max
                ):
                    errors.append(f"{output_path}.quantityMin cannot be greater than quantityMax.")

                if weight is not None and not is_positive_int(weight):
                    errors.append(f"{output_path}.weight must be a positive integer when present.")

        validate_tags(path, node.get("tags"), errors)


def validate_content(content: Any) -> list[str]:
    """Validate a Crafting Kit content object and return a list of errors."""
    errors: list[str] = []

    if not isinstance(content, dict):
        return ["Content pack must be a JSON object."]

    version = content.get("version")
    if not is_positive_int(version):
        errors.append("version must be a positive integer.")

    items = validate_id_map("items", content.get("items"), errors)
    recipes = validate_id_map("recipes", content.get("recipes"), errors)
    resource_nodes = validate_id_map("resourceNodes", content.get("resourceNodes"), errors)
    professions = validate_id_map("professions", content.get("professions"), errors)

    known_item_ids = validate_items(items, errors)
    known_profession_ids = validate_professions(professions, errors)
    validate_recipes(recipes, known_item_ids, known_profession_ids, errors)
    validate_resource_nodes(resource_nodes, known_item_ids, errors)

    return errors


def load_json_file(path: Path) -> Any:
    """Load JSON from disk."""
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Crafting Kit content JSON file.")
    parser.add_argument("path", type=Path, help="Path to a Crafting Kit JSON content file.")
    args = parser.parse_args()

    try:
        content = load_json_file(args.path)
    except OSError as error:
        print(f"Could not read file: {error}")
        return 2
    except json.JSONDecodeError as error:
        print(f"Could not parse JSON: {error}")
        return 2

    errors = validate_content(content)

    if errors:
        print("Crafting content is invalid:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Crafting content is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
