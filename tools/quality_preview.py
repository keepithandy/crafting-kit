"""Deterministic, read-only item quality preview."""
QUALITY = ("poor", "standard", "fine", "excellent", "masterwork")
def quality_preview(recipe, profession_level=0, tool_tier=0, quality="standard"):
    if quality not in QUALITY: return {"ok":False,"reason":"unknown_quality"}
    if not isinstance(profession_level,int) or not isinstance(tool_tier,int) or profession_level < 0 or tool_tier < 0: return {"ok":False,"reason":"malformed_modifiers"}
    index=QUALITY.index(quality); bonus=min(2,(profession_level//5)+(tool_tier//2)); tier=QUALITY[min(len(QUALITY)-1,index+bonus)]
    return {"ok":True,"tier":tier,"baseQuality":quality,"professionLevel":profession_level,"toolTier":tool_tier,"explanation":"deterministic explicit-input preview"}
