import json
import os
from typing import Any

from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from inventory import Inventory
from physical_product import PhysicalProduct
from product import Product
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
    """Create the correct Product subclass using the saved 'type' identifier."""
    product_type = item["type"]
    supplier = supplier_from_dict(item, suppliers)
    if product_type == "physical":
        return PhysicalProduct(item["id"], item["name"], item["price"],
                               item["stock"], item["weight"], supplier)
    if product_type == "digital":
        return DigitalProduct(item["id"], item["name"], item["price"],
                              item["stock"], item["download_size"], supplier)
    raise ValueError(f"Unknown product type: {product_type}")


def load_inventory(suppliers: dict[str, Supplier]) -> Inventory:
    """Load inventory.json into an Inventory object (empty if file missing/unreadable)."""
    inventory = Inventory()
    if os.path.exists(INVENTORY_FILE):
        try:
            with open(INVENTORY_FILE, "r") as file:
                data = json.load(file)
            for item in data:
                inventory.add_product(product_from_dict(item, suppliers))
            print("inventory.json found. Inventory loaded successfully.")
            return inventory
        except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError):
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


# Input helpers (validation carried over from earlier weeks)
def get_positive_int(prompt: str) -> int:
    """Keep asking until the user enters a whole number >= 0."""
    while True:
        entry = input(prompt).strip()
        if entry.isdigit():
            return int(entry)
        print(f"Error: '{entry}' is not a valid whole number. Try again.")


def get_positive_float(prompt: str) -> float:
    """Keep asking until the user enters a number >= 0."""
    while True:
        entry = input(prompt).strip()
        try:
            value = float(entry)
            if value >= 0:
                return value
            print("Error: value cannot be negative. Try again.")
        except ValueError:
            print(f"Error: '{entry}' is not a valid number. Try again.")


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
    stock = get_positive_int("Stock Quantity: ")
    supplier = get_supplier(suppliers)
    if supplier is None:
        return

    product: Product
    if product_type == "physical":
        weight = get_positive_float("Weight (kg): ")
        product = PhysicalProduct(product_id, name, price, stock, weight, supplier)
    else:
        download_size = get_positive_float("Download size (MB): ")
        product = DigitalProduct(product_id, name, price, stock, download_size, supplier)

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
    new_stock = get_positive_int("New Stock Quantity: ")
    if product.update_stock(new_stock):
        print("Stock updated successfully!")
    else:
        print("Error: stock could not be updated.")


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
        inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.2, tech_supply))
        inventory.add_product(PhysicalProduct("P002", "Mouse", 25.50, 40, 0.1, tech_supply))
        inventory.add_product(PhysicalProduct("P003", "Keyboard", 45.00, 25, 0.9, tech_supply))
        inventory.add_product(DigitalProduct("D001", "Photo Editor", 79.99, 500, 450.0, soft_house))
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
