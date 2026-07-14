"""Read-only Crafting Kit gathering dry-run helper."""

from __future__ import annotations


def gathering_dry_run(content, node_id, actor=None, inventory=None):
    """Preview a resource-node harvest without mutating inventory or content."""
    actor = actor or {}
    inventory = dict(inventory or {})
    resource_nodes = content.get("resourceNodes", {}) if isinstance(content, dict) else {}
    node = resource_nodes.get(node_id) if isinstance(resource_nodes, dict) else None

    if not isinstance(node, dict):
        return {"ok": False, "nodeId": node_id, "reason": "unknown_resource_node"}

    node_type = node.get("type")
    level_required = node.get("levelRequired", 1)
    actor_levels = actor.get("levels", {}) if isinstance(actor, dict) else {}
    actor_level = actor_levels.get(node_type, 1) if isinstance(actor_levels, dict) else 1

    if actor_level < level_required:
        return {
            "ok": False,
            "nodeId": node_id,
            "reason": "profession_level_too_low",
            "requiredLevel": level_required,
            "actorLevel": actor_level,
        }

    tool_required = node.get("toolRequired")
    if tool_required and inventory.get(tool_required, 0) <= 0:
        return {
            "ok": False,
            "nodeId": node_id,
            "reason": "missing_required_tool",
            "toolRequired": tool_required,
        }

    outputs_preview = []
    for output in node.get("outputs", []):
        outputs_preview.append(
            {
                "itemId": output.get("itemId"),
                "quantityMin": output.get("quantityMin"),
                "quantityMax": output.get("quantityMax"),
                "weight": output.get("weight", 1),
            }
        )

    return {
        "ok": True,
        "nodeId": node_id,
        "reason": "harvest_preview",
        "nodeType": node_type,
        "outputsPreview": outputs_preview,
        "inventoryAfterPreview": inventory,
    }
