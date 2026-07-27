"""Read-only starter-content economy summary."""
def economy_balance_report(content):
    items=content.get("items",{}) if isinstance(content,dict) else {}; recipes=content.get("recipes",{}) if isinstance(content,dict) else {}
    rows=[]; flags=[]
    for rid,recipe in recipes.items():
        input_value=sum(s.get("quantity",0)*items.get(s.get("itemId"),{}).get("value",0) for s in recipe.get("inputs",[]))
        output_value=sum(s.get("quantity",0)*items.get(s.get("itemId"),{}).get("value",0) for s in recipe.get("outputs",[]))
        missing=[s.get("itemId") for s in recipe.get("inputs",[])+recipe.get("outputs",[]) if "value" not in items.get(s.get("itemId"),{})]
        if missing: flags.append({"recipeId":rid,"type":"missing_values","items":missing})
        if input_value==0 and output_value>0: flags.append({"recipeId":rid,"type":"positive_value_without_input"})
        rows.append({"recipeId":rid,"inputValue":input_value,"outputValue":output_value,"delta":output_value-input_value})
    return {"recipes":rows,"flags":flags,"format":"structured"}
