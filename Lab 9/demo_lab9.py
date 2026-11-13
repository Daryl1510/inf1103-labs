"""Runs the Lab 9 'Predict first' scenarios so you can see the real output.
Run with: python demo_lab9.py   (write your predictions BEFORE you run it)
"""
import contextlib
import io
import os
import tempfile
from unittest.mock import patch

from discount_strategy import BulkDiscount, PercentageDiscount
from inventory import Inventory
from inventory_manager import get_positive_float
from order import Order
from product_factory import ProductFactory
from product_loader import load_products
from supplier import Supplier


def heading(text: str) -> None:
    print(f"\n=== {text} ===")


supplier = Supplier("S001", "TechSupply Co", "sales@techsupply.example")

# Section 2.3 - Strategy: an order whose lines add up to 250
heading("2.3 Strategy: order total 250")
keyboard = ProductFactory.create("physical", "P100", "Keyboard", 50.00, 20, supplier, weight=0.9)
order = Order("O1", BulkDiscount(200, 20))
order.add_order_line(keyboard, 5)                       # 5 x 50.00 = 250.00
print("With BulkDiscount(200, 20):  ", order.calculate_total())
order.set_discount(PercentageDiscount(10))
print("After set_discount(Percentage(10)):", order.calculate_total())

# Section 3.2 - Factory: an unknown product type (caught here so the demo can continue)
heading("3.2 Factory: unknown product type")
try:
    ProductFactory.create("service", "S001", "Installation", 30.00, 5, supplier)
except ValueError as error:
    print(f"ValueError raised by the factory: {error}")
print("(In the real program, if nothing caught it, the program would stop with a traceback.)")

# Section 5.1 - input helper with the user typing: abc, -5, 12.50
heading("5.1 Input helper: abc, then -5, then 12.50")
with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
    value = get_positive_float("Price: ")
print(f"Returned: {value}")

# Section 5.2 - loading products.csv (needs products.csv next to this file)
heading("5.2 Loading products.csv")
inventory = Inventory()
load_products("products.csv", inventory, supplier)
print("Product IDs in inventory:", [p.product_id for p in inventory.products])

heading("5.2 Loading again after products.csv is renamed (file missing)")
load_products("products_renamed.csv", Inventory(), supplier)
