"""Read-only inventory output-capacity preview."""
from math import ceil
def inventory_capacity_preview(content, recipe_id, inventory, slots, stack_limits=None):
    recipes=content.get("recipes",{}) if isinstance(content,dict) else {}; recipe=recipes.get(recipe_id) if isinstance(recipes,dict) else None
    if not isinstance(recipe,dict) or not isinstance(slots,int) or slots < 0: return {"ok":False,"reason":"invalid_input"}
    projected=dict(inventory or {}); missing=[]
    for stack in recipe.get("inputs",[]):
        available=projected.get(stack["itemId"],0); required=stack["quantity"]
        if available < required: missing.append({"itemId":stack["itemId"],"required":required,"available":available,"missing":required-available})
    if missing: return {"ok":False,"reason":"missing_materials","missing":missing,"inventoryAfterPreview":projected}
    for stack in recipe.get("inputs",[]): projected[stack["itemId"]]=projected.get(stack["itemId"],0)-stack["quantity"]
    for stack in recipe.get("outputs",[]): projected[stack["itemId"]]=projected.get(stack["itemId"],0)+stack["quantity"]
    limits=stack_limits or {}; used=sum(ceil(q/max(1,limits.get(item,99))) for item,q in projected.items() if q>0)
    return {"ok":used<=slots,"reason":"craftable" if used<=slots else "insufficient_output_capacity","usedSlots":used,"slots":slots,"inventoryAfterPreview":projected}
