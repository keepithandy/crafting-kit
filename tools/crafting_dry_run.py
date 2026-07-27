"""Read-only Crafting Kit recipe dry-run helper."""

from __future__ import annotations

from math import ceil


def _quantity(value):
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else 0


def crafting_batch_dry_run(content, recipe_id, inventory, quantity=1):
    """Preview multiple copies without mutating the supplied inventory."""
    if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
        return {"ok": False, "recipeId": recipe_id, "quantity": quantity, "reason": "invalid_quantity"}
    recipes = content.get("recipes", {}) if isinstance(content, dict) else {}
    recipe = recipes.get(recipe_id) if isinstance(recipes, dict) else None
    if not isinstance(recipe, dict):
        return {"ok": False, "recipeId": recipe_id, "quantity": quantity, "reason": "unknown_recipe"}
    safe = dict(inventory) if isinstance(inventory, dict) else {}
    required = {}
    for stack in recipe.get("inputs", []):
        item = stack.get("itemId"); required[item] = required.get(item, 0) + stack.get("quantity", 0) * quantity
    missing = [{"itemId": item, "required": amount, "available": _quantity(safe.get(item)), "missing": amount - _quantity(safe.get(item))}
               for item, amount in required.items() if _quantity(safe.get(item)) < amount]
    outputs = [{"itemId": s.get("itemId"), "quantity": s.get("quantity", 0) * quantity} for s in recipe.get("outputs", [])]
    after = dict(safe)
    if not missing:
        for item, amount in required.items(): after[item] = _quantity(after.get(item)) - amount
        for stack in outputs: after[stack["itemId"]] = _quantity(after.get(stack["itemId"])) + stack["quantity"]
    return {"ok": not missing, "recipeId": recipe_id, "quantity": quantity,
            "reason": "craftable" if not missing else "missing_materials", "missing": missing,
            "consumedPreview": [{"itemId": k, "quantity": v} for k, v in required.items()],
            "producedPreview": outputs, "inventoryAfterPreview": after}


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
