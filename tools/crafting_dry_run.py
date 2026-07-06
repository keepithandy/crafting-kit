"""Read-only Crafting Kit recipe dry-run helper."""

from __future__ import annotations


def crafting_dry_run(content, recipe_id, inventory):
    recipes = content.get("recipes", {}) if isinstance(content, dict) else {}
    recipe = recipes.get(recipe_id) if isinstance(recipes, dict) else None
    if not isinstance(recipe, dict):
        return {"ok": False, "recipeId": recipe_id, "reason": "unknown_recipe"}

    safe_inventory = dict(inventory)
    missing = []
    consumed = []
    produced = []

    for stack in recipe.get("inputs", []):
        item_id = stack.get("itemId")
        required = stack.get("quantity")
        available = safe_inventory.get(item_id, 0)
        consumed.append({"itemId": item_id, "quantity": required})
        if available < required:
            missing.append({"itemId": item_id, "required": required, "available": available, "missing": required - available})

    for stack in recipe.get("outputs", []):
        produced.append({"itemId": stack.get("itemId"), "quantity": stack.get("quantity")})

    if missing:
        return {
            "ok": False,
            "recipeId": recipe_id,
            "reason": "missing_materials",
            "missing": missing,
            "consumedPreview": consumed,
            "producedPreview": produced,
            "inventoryAfterPreview": safe_inventory,
        }

    inventory_after = dict(safe_inventory)
    for stack in consumed:
        inventory_after[stack["itemId"]] = inventory_after.get(stack["itemId"], 0) - stack["quantity"]
    for stack in produced:
        inventory_after[stack["itemId"]] = inventory_after.get(stack["itemId"], 0) + stack["quantity"]

    return {
        "ok": True,
        "recipeId": recipe_id,
        "reason": "craftable",
        "consumedPreview": consumed,
        "producedPreview": produced,
        "inventoryAfterPreview": inventory_after,
    }
