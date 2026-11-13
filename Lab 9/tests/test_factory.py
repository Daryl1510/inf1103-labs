"""Section 3 / 7: Factory pattern - creating products."""
import pathlib
import unittest

from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from product_factory import ProductFactory
from supplier import Supplier

PROJECT = pathlib.Path(__file__).resolve().parent.parent
SUPPLIER = Supplier("S1", "Test Supplier", "test@example.com")


class ProductFactoryTests(unittest.TestCase):
    def test_creates_physical_product(self) -> None:
        product = ProductFactory.create("physical", "P1", "Lamp", 25.0, 10, SUPPLIER, weight=1.5)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertIsInstance(product, Product)

    def test_creates_digital_product(self) -> None:
        product = ProductFactory.create("digital", "D1", "Editor", 49.9, 100, SUPPLIER,
                                        download_size=450.0)
        self.assertIsInstance(product, DigitalProduct)

    def test_unknown_type_raises_value_error_with_clear_message(self) -> None:
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S1", "Install", 30.0, 5, SUPPLIER)
        self.assertEqual(str(context.exception), "Unknown product type: service")

    def test_invalid_values_are_rejected_through_the_factory(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P1", "Lamp", 0, 10, SUPPLIER)
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D1", "Editor", 10, -1, SUPPLIER)

    def test_rest_of_program_never_creates_products_directly(self) -> None:
        for filename in ("inventory_manager.py", "product_loader.py"):
            source = (PROJECT / filename).read_text()
            self.assertNotIn("PhysicalProduct(", source, filename)
            self.assertNotIn("DigitalProduct(", source, filename)


if __name__ == "__main__":
    unittest.main()
