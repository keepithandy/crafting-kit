"""Read-only recipe dependency-cycle detection."""
def find_recipe_cycles(content):
    recipes = content.get("recipes", {}) if isinstance(content, dict) else {}
    producers = {}
    for recipe_id, recipe in recipes.items():
        for output in recipe.get("outputs", []): producers.setdefault(output.get("itemId"), []).append(recipe_id)
    graph = {recipe_id: set() for recipe_id in recipes}
    for recipe_id, recipe in recipes.items():
        for item in recipe.get("inputs", []): graph[recipe_id].update(producers.get(item.get("itemId"), []))
    cycles=[]; path=[]; active=set()
    def visit(node):
        if node in active:
            cycles.append(path[path.index(node):] + [node]); return
        active.add(node); path.append(node)
        for child in sorted(graph[node]): visit(child)
        path.pop(); active.remove(node)
    for node in sorted(graph): visit(node)
    return cycles
