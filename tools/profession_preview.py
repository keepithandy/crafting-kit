"""Read-only profession gate checks."""
def profession_requirement_preview(content, recipe_id, actor=None):
    recipes=content.get("recipes",{}) if isinstance(content,dict) else {}; recipe=recipes.get(recipe_id,{})
    required=recipe.get("levelRequired",0); profession=recipe.get("profession"); levels=(actor or {}).get("levels",{}) if isinstance(actor,dict) else {}; actual=levels.get(profession,0) if profession else 0
    ok=bool(profession) and isinstance(required,int) and isinstance(actual,int) and actual>=required
    return {"ok":ok,"reason":"craftable" if ok else ("missing_profession" if profession not in levels else "profession_level_too_low"),"profession":profession,"actorLevel":actual,"requiredLevel":required,"deficit":max(0,required-actual)}
