"""Section 2 / 7: Strategy pattern - discounts."""
import inspect
import unittest

from discount_strategy import BulkDiscount, DiscountStrategy, NoDiscount, PercentageDiscount
from order import Order
from physical_product import PhysicalProduct
from student_discount import StudentDiscount
from supplier import Supplier


def make_order_totalling_250(discount: DiscountStrategy | None = None) -> Order:
    supplier = Supplier("S1", "Test Supplier", "test@example.com")
    keyboard = PhysicalProduct("P1", "Keyboard", 50.00, 20, 0.9, supplier)
    order = Order("O1", discount) if discount is not None else Order("O1")
    order.add_order_line(keyboard, 5)           # 5 x 50.00 = 250.00
    return order


class DiscountStrategyTests(unittest.TestCase):
    def test_discount_strategy_is_abstract(self) -> None:
        with self.assertRaises(TypeError):
            DiscountStrategy()                   # type: ignore[abstract]

    def test_no_discount_returns_total_unchanged(self) -> None:
        self.assertEqual(NoDiscount().apply(250), 250)

    def test_percentage_discount(self) -> None:
        self.assertAlmostEqual(PercentageDiscount(10).apply(250), 225.0)

    def test_percentage_must_be_between_0_and_100(self) -> None:
        with self.assertRaises(ValueError):
            PercentageDiscount(150)

    def test_bulk_discount_applies_at_or_above_threshold(self) -> None:
        self.assertEqual(BulkDiscount(200, 20).apply(250), 230)
        self.assertEqual(BulkDiscount(200, 20).apply(200), 180)

    def test_bulk_discount_not_applied_below_threshold(self) -> None:
        self.assertEqual(BulkDiscount(200, 20).apply(199.99), 199.99)


class OrderUsesStrategyTests(unittest.TestCase):
    def test_default_order_has_no_discount(self) -> None:
        order = make_order_totalling_250()
        self.assertIsInstance(order.discount, NoDiscount)
        self.assertEqual(order.calculate_total(), 250)

    def test_order_calculates_total_through_its_strategy(self) -> None:
        order = make_order_totalling_250(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230)

    def test_set_discount_changes_strategy_on_existing_order(self) -> None:
        order = make_order_totalling_250(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230)
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.0)

    def test_order_has_no_discount_if_elif_logic(self) -> None:
        source = inspect.getsource(Order.calculate_total)
        self.assertNotIn("if ", source)
        self.assertNotIn("elif", source)

    def test_new_strategy_works_without_changing_order(self) -> None:
        order = make_order_totalling_250(StudentDiscount())
        self.assertAlmostEqual(order.calculate_total(), 237.5)

    def test_a_brand_new_strategy_defined_outside_order_also_works(self) -> None:
        class TenOffEverything(DiscountStrategy):
            def apply(self, total: float) -> float:
                return total - 10

        order = make_order_totalling_250(TenOffEverything())
        self.assertEqual(order.calculate_total(), 240)

    def test_one_strategy_object_can_be_shared_by_two_orders(self) -> None:
        shared = PercentageDiscount(10)
        first, second = make_order_totalling_250(shared), make_order_totalling_250(shared)
        self.assertIs(first.discount, second.discount)


if __name__ == "__main__":
    unittest.main()
