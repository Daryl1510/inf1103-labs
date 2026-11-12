"""Lab 8 checks (sections 2-7). Run with: python test_lab8.py

Each section has a PREDICT FIRST comment. Write your prediction in your Word
document BEFORE you run the script, then compare with the real output.
"""
from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order


def heading(text: str) -> None:
    print(f"\n=== {text} ===")


def show_product_details(product: Product) -> None:
    """Works for ANY Product - it never asks which subclass it is (LSP / polymorphism)."""
    product.display_information()
    print(f"    Fulfilment: {product.get_fulfilment_info()}")


# --------------------------------------------------------------------------
# Section 2: ASSOCIATION  (Supplier <-> Product)
# --------------------------------------------------------------------------
heading("2. Association: Supplier and Product")
supplier = Supplier("S001", "TechSupply Co", "sales@techsupply.example")
guitar = PhysicalProduct("P100", "Guitar", 450.00, 5, 3.5, supplier)
os_disk = DigitalProduct("D100", "Operating System", 129.99, 999, 4200.0, supplier)

print("Supplier information through each Product:")
guitar.display_supplier()
os_disk.display_supplier()

print("Same Supplier object behind both products:", guitar.supplier is os_disk.supplier)
print("That object is the one we created:", guitar.supplier is supplier)

# PREDICT FIRST: what happens to the products' supplier information after `del supplier`?
heading("2. Predict first: del supplier")
del supplier                       # removes only the NAME 'supplier', not the object
print("After del supplier, products can still show their supplier:")
guitar.display_supplier()
os_disk.display_supplier()


# --------------------------------------------------------------------------
# Section 3: AGGREGATION  (Inventory <>-- Product)
# --------------------------------------------------------------------------
heading("3. Aggregation: Inventory and Product")
tech = guitar.supplier                              # re-use the same supplier object
mouse = PhysicalProduct("P101", "Mouse", 25.50, 40, 0.1, tech)   # exists BEFORE any inventory
inventory_a = Inventory()
inventory_b = Inventory()

inventory_a.add_product(mouse)
inventory_a.add_product(os_disk)
print("Inventory A after adding Mouse and OS:", [p.product_id for p in inventory_a.products])

# PREDICT FIRST: will the Product still work after it is removed from Inventory A?
heading("3. Predict first: remove from Inventory A")
removed = inventory_a.remove_product("P101")
print("Inventory A now:", [p.product_id for p in inventory_a.products])
print("Mouse still usable after removal:")
mouse.display_information()
print("Mouse can still change its own stock:", mouse.update_stock(35), "-> stock", mouse.stock)
print("remove_product returned the same object:", removed is mouse)

inventory_b.add_product(mouse)
print("Inventory B after adding the same Mouse:", [p.product_id for p in inventory_b.products])
print("Same object in B:", inventory_b.find_product("P101") is mouse)

print("find_product on a missing ID:", inventory_a.find_product("NOPE"))

heading("3. Emptying an inventory does not destroy products")
inventory_a.remove_product("D100")
print("Inventory A empty:", inventory_a.is_empty())
print("os_disk still works:")
os_disk.display_information()


# --------------------------------------------------------------------------
# Section 4: COMPOSITION  (Order <#>-- OrderLine)
# --------------------------------------------------------------------------
heading("4. Composition: Order and OrderLine")
order_1 = Order("O001")
order_1.add_order_line(guitar, 1)
order_1.add_order_line(mouse, 2)
order_1.add_order_line(os_disk, 1)
order_1.display_information()
print(f"Order total: ${order_1.calculate_total():.2f}")

# PREDICT FIRST: same Product in two Orders -> how many OrderLines? how many Products?
heading("4. Predict first: same Product in two Orders")
order_2 = Order("O002")
order_2.add_order_line(guitar, 3)
line_in_1 = order_1.order_lines[0]       # the Guitar line of order 1
line_in_2 = order_2.order_lines[0]       # the Guitar line of order 2
print("Order lines are different objects:", line_in_1 is not line_in_2,
      f"(ids {id(line_in_1)} vs {id(line_in_2)})")
print("Both lines refer to the SAME Product:", line_in_1.product is line_in_2.product,
      f"(ids {id(line_in_1.product)} vs {id(line_in_2.product)})")
order_2.display_information()

heading("4. Order manages its own lines")
print("Remove Mouse line from order 1:", order_1.remove_order_line("P101"))
print("Remove a line that is not there:", order_1.remove_order_line("P999"))
order_1.display_information()

print("\nCancel order 2 -> its lines go with it, the Product does not:")
order_2.cancel()
order_2.display_information()
print("Guitar is still fine:")
guitar.display_information()


# --------------------------------------------------------------------------
# Section 6: LSP
# --------------------------------------------------------------------------
heading("6. LSP: show_product_details() with both product types")
show_product_details(guitar)
show_product_details(os_disk)

heading("6. LSP: both subclasses keep Product's update_stock() contract")
for item in (guitar, os_disk):
    print(f"{type(item).__name__}: update_stock(10) ->", item.update_stock(10),
          "| update_stock(-5) ->", item.update_stock(-5), "| stock is", item.stock)

heading("6. Diagnose: a subclass that BREAKS the Product contract (demo only)")


class BadDigitalProduct(DigitalProduct):
    """The teammate's proposal. NOT used by the real system - for demonstration.

    A static type checker (mypy) also flags this class: its update_stock() returns
    None where Product promises bool - the same LSP problem, caught before running.
    """

    def update_stock(self, quantity: int) -> None:
        raise NotImplementedError("Digital products have no stock")


bad = BadDigitalProduct("D999", "Bad Software", 9.99, 10, 50.0, tech)
try:
    # Code written for Product expects update_stock() to work on any Product:
    bad.update_stock(5)
    print("worked")
except NotImplementedError as error:
    print(f"LSP VIOLATION - code that works for Product breaks for the subclass: {error}")


# --------------------------------------------------------------------------
# Section 7: POLYMORPHISM through the Product abstraction
# --------------------------------------------------------------------------
heading("7. Polymorphism: one Inventory, one loop, both product types")
shop = Inventory()
shop.add_product(guitar)
shop.add_product(mouse)
shop.add_product(os_disk)

# PREDICT FIRST: what will get_fulfilment_info() print for each product?
# One loop, no isinstance(): each object supplies its own behaviour.
for product in shop.products:
    product.display_information()
    print(f"    Fulfilment: {product.get_fulfilment_info()}")

heading("Inventory.display_all() also works polymorphically")
shop.display_all()
