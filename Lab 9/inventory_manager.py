import json
import math
import os
from typing import Any

from can_be_shipped import CanBeShipped
from inventory import Inventory
from product import Product
from product_factory import ProductFactory
from supplier import Supplier

DATA_DIR = "data"
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.json")


# File Handling (loads/saves data; converts between JSON dictionaries and objects)
# JSON data read from a file has no fixed shape, so dict[str, Any] is used ONLY for
# those two from_dict functions. Everything else uses specific types.
# Suppliers are kept in a dictionary {supplier_id: Supplier} so that products from the
# same supplier share ONE Supplier object (association: many products -> one supplier).
LEGACY_SUPPLIER = Supplier("S000", "Unknown Supplier", "not-provided@example.com")


def supplier_from_dict(item: dict[str, Any], suppliers: dict[str, Supplier]) -> Supplier:
    """Reuse an existing Supplier with the same ID, or create it if it is new.
    Files saved in Lab 7 have no supplier, so they get a default 'Unknown Supplier'."""
    data = item.get("supplier")
    if data is None:
        suppliers.setdefault(LEGACY_SUPPLIER.supplier_id, LEGACY_SUPPLIER)
        return suppliers[LEGACY_SUPPLIER.supplier_id]
    supplier_id = data["supplier_id"]
    if supplier_id not in suppliers:
        suppliers[supplier_id] = Supplier(supplier_id, data["name"], data["contact_email"])
    return suppliers[supplier_id]


def product_from_dict(item: dict[str, Any], suppliers: dict[str, Supplier]) -> Product:
    """Create the correct Product through the factory, using the saved 'type'.
    Raises ValueError for an unknown type or invalid values, KeyError if a field is missing."""
    supplier = supplier_from_dict(item, suppliers)
    return ProductFactory.create(item["type"], item["id"], item["name"], item["price"],
                                 item["stock"], supplier,
                                 weight=item.get("weight", 0.0),
                                 download_size=item.get("download_size", 0.0))


def load_inventory(suppliers: dict[str, Supplier]) -> Inventory:
    """Load inventory.json into an Inventory object (empty if file missing/unreadable)."""
    inventory = Inventory()
    if os.path.exists(INVENTORY_FILE):
        try:
            with open(INVENTORY_FILE, "r") as file:
                data = json.load(file)
            for item in data:
                try:
                    inventory.add_product(product_from_dict(item, suppliers))
                except (KeyError, TypeError, ValueError) as error:
                    # one bad product is reported and skipped, the rest still load
                    print(f"Skipping a saved product that could not be loaded: {error!r}")
            print("inventory.json found. Inventory loaded successfully.")
            return inventory
        except (json.JSONDecodeError, OSError, TypeError):
            print("inventory.json could not be read. Starting with an empty inventory.")
            suppliers.clear()
            return Inventory()
    print("No inventory.json found. Starting with an empty inventory.")
    return inventory


def save_inventory(inventory: Inventory) -> None:
    """Write the inventory to inventory.json."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(INVENTORY_FILE, "w") as file:
        json.dump(inventory.to_list(), file, indent=4)
    print("Inventory saved successfully to inventory.json.")


# Input helpers: they keep asking until the user gives a valid value, and never crash.
# They catch ValueError because int()/float() raise it for text that is not a number,
# and our own validation can too (exception handling + validation working together).
def get_non_negative_int(prompt: str) -> int:
    """Keep asking until the user enters a whole number that is 0 or more."""
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter a whole number that is 0 or more.")
                continue
            return value
        except ValueError:
            print("Please enter a valid whole number, e.g. 10")


def get_positive_float(prompt: str) -> float:
    """Keep asking until the user enters a number greater than zero."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0 or not math.isfinite(value):     # also rejects nan and inf
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def get_product_type() -> str:
    """Ask the user to choose a product type. Returns 'physical' or 'digital'."""
    while True:
        print("Product Type:")
        print("  1. Physical")
        print("  2. Digital")
        choice = input("Choose type (1 or 2): ").strip()
        if choice == "1":
            return "physical"
        if choice == "2":
            return "digital"
        print("Error: please enter 1 or 2.")


def get_supplier(suppliers: dict[str, Supplier]) -> Supplier | None:
    """Ask for a supplier ID. Reuse a known supplier, or create a new one.
    Returns None if the user leaves the ID empty."""
    supplier_id = input("Supplier ID: ").strip().upper()
    if supplier_id == "":
        print("Error: Supplier ID cannot be empty.")
        return None
    if supplier_id in suppliers:
        print("Existing supplier found:")
        suppliers[supplier_id].display_information()
        return suppliers[supplier_id]
    name = input("New supplier name: ").strip()
    email = input("New supplier contact email: ").strip()
    if name == "" or email == "":
        print("Error: supplier name and email cannot be empty.")
        return None
    suppliers[supplier_id] = Supplier(supplier_id, name, email)
    return suppliers[supplier_id]


# Menu actions (get user input, then call Inventory / Product methods)
def add_product(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()

    if product_id == "":
        print("Error: Product ID cannot be empty.")
        return
    if inventory.find_product(product_id) is not None:
        print(f"Error: Product ID {product_id} already exists.")
        return

    name = input("Product Name: ").strip()
    if name == "":
        print("Error: Product name cannot be empty.")
        return

    product_type = get_product_type()
    price = get_positive_float("Price: ")
    stock = get_non_negative_int("Stock Quantity: ")
    supplier = get_supplier(suppliers)
    if supplier is None:
        return

    # Ask for the detail that belongs to this type, then let the FACTORY build it.
    weight = 0.0
    download_size = 0.0
    if product_type == "physical":
        weight = get_positive_float("Weight (kg): ")
    else:
        download_size = get_positive_float("Download size (MB): ")

    try:
        product = ProductFactory.create(product_type, product_id, name, price, stock,
                                        supplier, weight=weight, download_size=download_size)
    except ValueError as error:
        print(f"Error: {error}")
        return

    inventory.add_product(product)
    print("Product added successfully!")


def update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print(f"\nProduct Found: Name: {product.name} Current Stock: {product.stock}")
    new_stock = get_non_negative_int("New Stock Quantity: ")
    try:
        product.update_stock(new_stock)
    except ValueError as error:
        print(f"Error: {error}")
        return
    print("Stock updated successfully!")


def search_product(inventory: Inventory) -> None:
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print("Product Found")
    product.display_information()
    print(f"    Fulfilment: {product.get_fulfilment_info()}")
    print("    Supplier: ", end="")
    product.display_supplier()
    # Only products that sign the CanBeShipped interface can quote shipping.
    if isinstance(product, CanBeShipped):
        print(f"    Shipping cost: ${product.calculate_shipping_cost():.2f}")


# Menu System
def show_menu() -> None:
    print("\nMENU")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")


def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    print()

    suppliers: dict[str, Supplier] = {}      # every known supplier, by ID
    inventory = load_inventory(suppliers)

    # Starter data: only used the very first time (no saved file yet).
    # Suppliers are created first, independently, then handed to the products.
    if inventory.is_empty():
        tech_supply = Supplier("S001", "TechSupply Co", "sales@techsupply.example")
        soft_house = Supplier("S002", "SoftHouse Ltd", "hello@softhouse.example")
        suppliers[tech_supply.supplier_id] = tech_supply
        suppliers[soft_house.supplier_id] = soft_house
        inventory.add_product(ProductFactory.create(
            "physical", "P001", "Laptop", 1200.00, 15, tech_supply, weight=2.2))
        inventory.add_product(ProductFactory.create(
            "physical", "P002", "Mouse", 25.50, 40, tech_supply, weight=0.1))
        inventory.add_product(ProductFactory.create(
            "physical", "P003", "Keyboard", 45.00, 25, tech_supply, weight=0.9))
        inventory.add_product(ProductFactory.create(
            "digital", "D001", "Photo Editor", 79.99, 500, soft_house, download_size=450.0))
        print("Loaded 4 starter products.")

    while True:
        show_menu()
        choice = input("\nEnter option: ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product(inventory, suppliers)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            print("Saving inventory...")
            save_inventory(inventory)
        elif choice == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("\nThank you for using Inventory Management System. "
                  "Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
