/*
 * Read-only browser controller for the Crafting Kit prototype.
 *
 * This is a replaceable UI layer over the Python/data contracts. It owns
 * selection state and rendering only; it never mutates inventory or performs
 * a live crafting action.
 */
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

// This is UI selection state, not player or inventory state.
const state = { selectedRecipeId: recipes[0].id };

function itemLabel(itemId) {
  return itemId.replaceAll("_", " ");
}

function getSelectedRecipe() {
  return recipes.find((recipe) => recipe.id === state.selectedRecipeId) || recipes[0];
}

function previewRecipe(recipe, inventoryState) {
  const requirements = recipe.inputs.map(([itemId, required]) => {
    const available = inventoryState[itemId] || 0;
    return { itemId, required, available, ready: available >= required };
  });

  return Object.freeze({
    recipeId: recipe.id,
    requirements: Object.freeze(requirements),
    craftable: requirements.every((requirement) => requirement.ready),
    output: recipe.output,
  });
}

function selectRecipe(recipeId) {
  if (!recipes.some((recipe) => recipe.id === recipeId)) return;
  state.selectedRecipeId = recipeId;
  render();
}

function renderRecipes() {
  const grid = document.getElementById("recipeGrid");
  grid.replaceChildren();

  recipes.forEach((recipe) => {
    const preview = previewRecipe(recipe, inventory);
    const button = document.createElement("button");
    const selected = recipe.id === state.selectedRecipeId;
    button.type = "button";
    button.className = `recipe-card ${selected ? "selected" : ""}`;
    button.setAttribute("aria-pressed", String(selected));
    button.setAttribute("aria-label", `Select ${recipe.name}`);
    button.innerHTML = `<span class="pill">${recipe.profession}</span><h3>${recipe.name}</h3><p>${recipe.inputs.map(([itemId, quantity]) => `${quantity} ${itemLabel(itemId)}`).join(", ")}</p><strong class="${preview.craftable ? "ok" : "blocked"}">${preview.craftable ? "Craftable" : "Blocked: missing materials"}</strong>`;
    button.addEventListener("click", () => selectRecipe(recipe.id));
    grid.appendChild(button);
  });
}

function renderInventory() {
  const grid = document.getElementById("inventoryGrid");
  grid.innerHTML = Object.entries(inventory)
    .map(([itemId, quantity]) => `<div class="inventory-card"><strong>${itemLabel(itemId)}</strong><p>${quantity} available</p></div>`)
    .join("");
}

function renderRecipeDetail(recipe, preview) {
  const detail = document.getElementById("recipeDetail");
  detail.innerHTML = `<h3>${recipe.name}</h3><dl class="summary-list"><div><dt>Profession</dt><dd>${recipe.profession}</dd></div><div><dt>Output</dt><dd>${itemLabel(preview.output)}</dd></div></dl><h4>Requirements</h4><ul class="detail-list">${preview.requirements.map((requirement) => `<li class="requirement-row"><span>${itemLabel(requirement.itemId)}</span><strong class="${requirement.ready ? "ok" : "blocked"}">${requirement.available} / ${requirement.required} available</strong></li>`).join("")}</ul>`;
}

function renderResult(recipe, preview) {
  const result = document.getElementById("resultCard");
  result.innerHTML = `<h3>${recipe.name}</h3><p>Output preview: <strong>${itemLabel(preview.output)}</strong></p><span class="preview-badge ${preview.craftable ? "ok" : "blocked"}">${preview.craftable ? "Preview available" : "Preview blocked"}</span><p class="status-line ${preview.craftable ? "ok" : "blocked"}" role="status">${preview.craftable ? "All required materials are present." : "One or more required materials are missing."}</p>`;
}

function render() {
  const recipe = getSelectedRecipe();
  const preview = previewRecipe(recipe, inventory);
  renderRecipes();
  renderRecipeDetail(recipe, preview);
  renderInventory();
  renderResult(recipe, preview);
}

const controller = Object.freeze({
  getState: () => Object.freeze({ selectedRecipeId: state.selectedRecipeId }),
  previewRecipe,
  selectRecipe,
  render,
});

if (typeof window !== "undefined") window.CraftingKitPrototype = controller;

render();
