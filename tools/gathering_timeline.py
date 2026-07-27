"""Deterministic resource depletion and respawn preview."""
def gathering_timeline_preview(node, harvested=0, now=0):
    if not isinstance(node,dict): return {"ok":False,"reason":"invalid_node"}
    charges=node.get("depletionCount",node.get("charges",1)); respawn=node.get("respawnSeconds",0)
    if not isinstance(charges,int) or charges<=0 or not isinstance(respawn,int) or respawn<0 or not isinstance(harvested,int) or harvested<0:
        return {"ok":False,"reason":"invalid_depletion_fields"}
    remaining=max(0,charges-harvested); depleted=remaining==0
    return {"ok":True,"harvestCount":min(harvested,charges),"remainingCharges":remaining,"blocked":depleted,"nextReadyAt":now+respawn if depleted else None}
