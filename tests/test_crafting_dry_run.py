import json
import unittest
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.crafting_dry_run import crafting_dry_run


class CraftingDryRunTests(unittest.TestCase):
    def setUp(self):
        with (ROOT / "examples" / "starter-content.json").open("r", encoding="utf-8") as file:
            self.content = json.load(file)

    def test_recipe_is_craftable_without_mutating_inventory(self):
        inventory = {"iron_ore": 3, "coal": 1}
        result = crafting_dry_run(self.content, "iron_ingot_from_ore", inventory)

        self.assertTrue(result["ok"])
        self.assertEqual(inventory, {"iron_ore": 3, "coal": 1})
        self.assertEqual(result["inventoryAfterPreview"]["iron_ore"], 0)
        self.assertEqual(result["inventoryAfterPreview"]["coal"], 0)
        self.assertEqual(result["inventoryAfterPreview"]["iron_ingot"], 1)

    def test_missing_materials_are_reported(self):
        result = crafting_dry_run(self.content, "iron_ingot_from_ore", {"iron_ore": 1, "coal": 0})

        self.assertFalse(result["ok"])
        self.assertEqual(result["reason"], "missing_materials")
        self.assertEqual(result["missing"][0]["itemId"], "iron_ore")
        self.assertEqual(result["missing"][0]["missing"], 2)

    def test_unknown_recipe_is_readable(self):
        result = crafting_dry_run(self.content, "missing_recipe", {})

        self.assertFalse(result["ok"])
        self.assertEqual(result["reason"], "unknown_recipe")


if __name__ == "__main__":
    unittest.main()
