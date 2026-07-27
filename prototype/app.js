/* Read-only browser controller for the Crafting Kit prototype. */
const inventory = Object.freeze({
  iron_ore: 3,
  coal: 1,
  wild_herb: 1,
  water_vial: 1,
  cloth_scrap: 4,
  thread: 2,
});

const recipes = Object.freeze([
  { id: "iron_ingot_from_ore", name: "Smelt Iron Ingot", profession: "Blacksmithing", inputs: [["iron_ore", 3], ["coal", 1]], output: "iron_ingot" },
  { id: "brew_healing_potion", name: "Brew Healing Potion", profession: "Alchemy", inputs: [["wild_herb", 2], ["water_vial", 1]], output: "healing_potion" },
  { id: "stitch_simple_cloak", name: "Stitch Simple Cloak", profession: "Tailoring", inputs: [["cloth_scrap", 4], ["thread", 2]], output: "simple_cloak" },
]);

let selectedRecipe = recipes[0];

function canCraft(recipe) {
  return recipe.inputs.every(([itemId, quantity]) => (inventory[itemId] || 0) >= quantity);
}

function itemLabel(itemId) {
  return itemId.replaceAll("_", " ");
}

function renderRecipes() {
  const grid = document.getElementById("recipeGrid");
  grid.replaceChildren();

  recipes.forEach((recipe) => {
    const button = document.createElement("button");
    const craftable = canCraft(recipe);
    button.type = "button";
    button.className = `recipe-card ${recipe.id === selectedRecipe.id ? "selected" : ""}`;
    button.setAttribute("aria-pressed", String(recipe.id === selectedRecipe.id));
    button.setAttribute("aria-label", `Select ${recipe.name}`);
    button.innerHTML = `<span class="pill">${recipe.profession}</span><h3>${recipe.name}</h3><p>${recipe.inputs.map(([itemId, quantity]) => `${quantity} ${itemLabel(itemId)}`).join(", ")}</p><strong class="${craftable ? "ok" : "blocked"}">${craftable ? "Craftable" : "Blocked: missing materials"}</strong>`;
    button.addEventListener("click", () => { selectedRecipe = recipe; render(); });
    grid.appendChild(button);
  });
}

function renderInventory() {
  const grid = document.getElementById("inventoryGrid");
  grid.innerHTML = Object.entries(inventory)
    .map(([itemId, quantity]) => `<div class="inventory-card"><strong>${itemLabel(itemId)}</strong><p>${quantity} available</p></div>`)
    .join("");
}

function renderRecipeDetail() {
  const detail = document.getElementById("recipeDetail");
  detail.innerHTML = `<h3>${selectedRecipe.name}</h3><dl class="summary-list"><div><dt>Profession</dt><dd>${selectedRecipe.profession}</dd></div><div><dt>Output</dt><dd>${itemLabel(selectedRecipe.output)}</dd></div></dl><h4>Requirements</h4><ul class="detail-list">${selectedRecipe.inputs.map(([itemId, quantity]) => { const available = inventory[itemId] || 0; const ready = available >= quantity; return `<li class="requirement-row"><span>${itemLabel(itemId)}</span><strong class="${ready ? "ok" : "blocked"}">${available} / ${quantity} available</strong></li>`; }).join("")}</ul>`;
}

function renderResult() {
  const result = document.getElementById("resultCard");
  const craftable = canCraft(selectedRecipe);
  result.innerHTML = `<h3>${selectedRecipe.name}</h3><p>Output preview: <strong>${itemLabel(selectedRecipe.output)}</strong></p><span class="preview-badge ${craftable ? "ok" : "blocked"}">${craftable ? "Preview available" : "Preview blocked"}</span><p class="status-line ${craftable ? "ok" : "blocked"}" role="status">${craftable ? "All required materials are present." : "One or more required materials are missing."}</p>`;
}

function render() {
  renderRecipes();
  renderRecipeDetail();
  renderInventory();
  renderResult();
}

render();
