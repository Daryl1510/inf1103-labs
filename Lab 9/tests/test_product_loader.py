"""Section 5.2 / 7: loading products from CSV, and every except being specific."""
import contextlib
import io
import os
import pathlib
import re
import tempfile
import unittest

from inventory import Inventory
from product_loader import load_products
from supplier import Supplier

PROJECT = pathlib.Path(__file__).resolve().parent.parent
SUPPLIER = Supplier("S1", "Test Supplier", "test@example.com")


def load(path: str) -> tuple[Inventory, list[str]]:
    inventory = Inventory()
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        load_products(path, inventory, SUPPLIER)
    return inventory, output.getvalue().splitlines()


class LoadProductsTests(unittest.TestCase):
    def test_assignment_file_loads_good_rows_and_skips_bad_ones(self) -> None:
        inventory, lines = load(str(PROJECT / "products.csv"))
        self.assertEqual([p.product_id for p in inventory.products], ["P001", "D001", "P003"])
        self.assertEqual(lines, [
            "Skipping row 4: Unknown product type: service",
            "Skipping row 5: could not convert string to float: 'abc'",
            "3 products loaded.",
            "Load attempt finished.",
        ])

    def test_missing_file_is_handled_without_crashing(self) -> None:
        inventory, lines = load("no_such_file.csv")
        self.assertTrue(inventory.is_empty())
        self.assertEqual(lines, ["Products file not found: no_such_file.csv",
                                 "Load attempt finished."])

    def test_negative_stock_row_is_skipped_but_valid_rows_still_load(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "p.csv")
            with open(path, "w") as file:
                file.write("product_type,product_id,name,price,stock_quantity\n"
                           "physical,P1,Lamp,10,-4\n"
                           "digital,D1,Editor,5,3\n"
                           "physical,P2,Short row\n"
                           "\n"
                           "digital,D1,Duplicate,5,3\n")
            inventory, lines = load(path)
        self.assertEqual([p.product_id for p in inventory.products], ["D1"])
        self.assertIn("Skipping row 2: Stock quantity cannot be negative.", lines)
        self.assertTrue(any(line.startswith("Skipping row 4:") for line in lines))
        self.assertIn("Skipping row 6: ID D1 already exists.", lines)
        self.assertEqual(lines[-2:], ["1 products loaded.", "Load attempt finished."])


class ExceptionStyleTests(unittest.TestCase):
    def test_every_except_names_a_specific_exception(self) -> None:
        for source_file in PROJECT.glob("*.py"):
            for line_number, line in enumerate(source_file.read_text().splitlines(), 1):
                stripped = line.strip()
                if stripped.startswith("except"):
                    self.assertIsNone(re.match(r"except\s*:", stripped),
                                      f"bare except in {source_file.name}:{line_number}")
                    self.assertNotRegex(stripped, r"except\s+(Base)?Exception\b",
                                        f"too broad in {source_file.name}:{line_number}")


if __name__ == "__main__":
    unittest.main()
