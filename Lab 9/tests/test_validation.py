"""Section 4 / 7: validation of price, stock and order quantity."""
import unittest

from digital_product import DigitalProduct
from order import Order
from order_line import OrderLine
from physical_product import PhysicalProduct
from supplier import Supplier

SUPPLIER = Supplier("S1", "Test Supplier", "test@example.com")


class PriceValidationTests(unittest.TestCase):
    def test_price_must_be_greater_than_zero(self) -> None:
        for bad_price in (0, -5, float("nan")):
            with self.assertRaises(ValueError):
                PhysicalProduct("P1", "Lamp", bad_price, 10, 1.0, SUPPLIER)

    def test_digital_product_obeys_the_same_price_rule(self) -> None:     # LSP
        with self.assertRaises(ValueError):
            DigitalProduct("D1", "Editor", 0, 10, 100.0, SUPPLIER)


class StockValidationTests(unittest.TestCase):
    def test_new_product_stock_cannot_be_negative(self) -> None:
        with self.assertRaises(ValueError):
            PhysicalProduct("P1", "Lamp", 10.0, -1, 1.0, SUPPLIER)

    def test_zero_stock_is_allowed(self) -> None:
        self.assertEqual(PhysicalProduct("P1", "Lamp", 10.0, 0, 1.0, SUPPLIER).stock, 0)

    def test_update_stock_rejects_negative_and_keeps_old_value(self) -> None:
        for product in (PhysicalProduct("P1", "Lamp", 10.0, 5, 1.0, SUPPLIER),
                        DigitalProduct("D1", "Editor", 10.0, 5, 100.0, SUPPLIER)):
            with self.assertRaises(ValueError):
                product.update_stock(-5)
            self.assertEqual(product.stock, 5)          # unchanged

    def test_update_stock_rejects_non_whole_numbers(self) -> None:
        product = PhysicalProduct("P1", "Lamp", 10.0, 5, 1.0, SUPPLIER)
        with self.assertRaises(ValueError):
            product.update_stock(2.5)                    # type: ignore[arg-type]

    def test_update_stock_accepts_valid_value(self) -> None:
        product = DigitalProduct("D1", "Editor", 10.0, 5, 100.0, SUPPLIER)
        product.update_stock(10)
        self.assertEqual(product.stock, 10)


class OrderQuantityValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.product = PhysicalProduct("P1", "Lamp", 10.0, 5, 1.0, SUPPLIER)

    def test_order_line_quantity_must_be_greater_than_zero(self) -> None:
        for bad_quantity in (0, -3):
            with self.assertRaises(ValueError):
                OrderLine(self.product, bad_quantity)

    def test_order_rejects_bad_quantity_and_adds_no_line(self) -> None:
        order = Order("O1")
        with self.assertRaises(ValueError):
            order.add_order_line(self.product, 0)
        self.assertEqual(order.order_lines, [])


if __name__ == "__main__":
    unittest.main()
