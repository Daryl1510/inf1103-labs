import json
import os

from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from inventory import Inventory
from physical_product import PhysicalProduct

DATA_DIR = "data"
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.json")


# File Handling (loads/saves data; converts between JSON dictionaries and objects)
def product_from_dict(item):
    """Create the correct Product subclass using the saved 'type' identifier."""
    product_type = item["type"]
    if product_type == "physical":
        return PhysicalProduct(item["id"], item["name"], item["price"],
                               item["stock"], item["weight"])
    if product_type == "digital":
        return DigitalProduct(item["id"], item["name"], item["price"],
                              item["stock"], item["download_size"])
    raise ValueError(f"Unknown product type: {product_type}")


def load_inventory():
    """Load inventory.json into an Inventory object (empty if file missing/unreadable)."""
    inventory = Inventory()
    if os.path.exists(INVENTORY_FILE):
        try:
            with open(INVENTORY_FILE, "r") as file:
                data = json.load(file)
            for item in data:
                inventory.add_product(product_from_dict(item))
            print("inventory.json found. Inventory loaded successfully.")
            return inventory
        except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError):
            print("inventory.json could not be read. Starting with an empty inventory.")
            return Inventory()
    print("No inventory.json found. Starting with an empty inventory.")
    return inventory


def save_inventory(inventory):
    """Write the inventory to inventory.json."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(INVENTORY_FILE, "w") as file:
        json.dump(inventory.to_list(), file, indent=4)
    print("Inventory saved successfully to inventory.json.")


# Input helpers (validation carried over from earlier weeks)
def get_positive_int(prompt):
    """Keep asking until the user enters a whole number >= 0."""
    while True:
        entry = input(prompt).strip()
        if entry.isdigit():
            return int(entry)
        print(f"Error: '{entry}' is not a valid whole number. Try again.")


def get_positive_float(prompt):
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


def get_product_type():
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


# Menu actions (get user input, then call Inventory / Product methods)
def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()

    if product_id == "":
        print("Error: Product ID cannot be empty.")
        return
    if inventory.search_product(product_id) is not None:
        print(f"Error: Product ID {product_id} already exists.")
        return

    name = input("Product Name: ").strip()
    if name == "":
        print("Error: Product name cannot be empty.")
        return

    product_type = get_product_type()
    price = get_positive_float("Price: ")
    stock = get_positive_int("Stock Quantity: ")

    if product_type == "physical":
        weight = get_positive_float("Weight (kg): ")
        product = PhysicalProduct(product_id, name, price, stock, weight)
    else:
        download_size = get_positive_float("Download size (MB): ")
        product = DigitalProduct(product_id, name, price, stock, download_size)

    inventory.add_product(product)
    print("Product added successfully!")


def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print(f"\nProduct Found: Name: {product.name} Current Stock: {product.stock}")
    new_stock = get_positive_int("New Stock Quantity: ")
    if product.update_stock(new_stock):
        print("Stock updated successfully!")
    else:
        print("Error: stock could not be updated.")


def search_product(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print("Product Found")
    product.display_information()
    print(f"    Fulfilment: {product.get_fulfilment_info()}")
    # Only products that sign the CanBeShipped interface can quote shipping.
    if isinstance(product, CanBeShipped):
        print(f"    Shipping cost: ${product.calculate_shipping_cost():.2f}")


# Menu System
def show_menu():
    print("\nMENU")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    print()

    inventory = load_inventory()

    # Starter data: only used the very first time (no saved file yet)
    if inventory.is_empty():
        inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.2))
        inventory.add_product(PhysicalProduct("P002", "Mouse", 25.50, 40, 0.1))
        inventory.add_product(PhysicalProduct("P003", "Keyboard", 45.00, 25, 0.9))
        inventory.add_product(DigitalProduct("D001", "Photo Editor", 79.99, 500, 450.0))
        print("Loaded 4 starter products.")

    while True:
        show_menu()
        choice = input("\nEnter option: ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product(inventory)
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
