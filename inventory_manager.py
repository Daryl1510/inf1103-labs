import json
import os

DATA_DIR = "data"
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.json")



# Data Persistence
def load_inventory():
    """Load inventory.json if it exists, otherwise start with an empty list."""
    if os.path.exists(INVENTORY_FILE):
        try:
            with open(INVENTORY_FILE, "r") as file:
                inventory = json.load(file)
            print("inventory.json found. Inventory loaded successfully.")
            return inventory
        except (json.JSONDecodeError, OSError):
            print("inventory.json could not be read. Starting with an empty inventory.")
            return []
    print("No inventory.json found. Starting with an empty inventory.")
    return []


def save_inventory(inventory):
    """Write the inventory list to inventory.json."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(INVENTORY_FILE, "w") as file:
        json.dump(inventory, file, indent=4)
    print("Inventory saved successfully to inventory.json.")



# Input helpers (validation carried over from last week)
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


# Data Manipulation
def find_product(inventory, product_id):
    """Return the product dictionary with this ID, or None."""
    for product in inventory:
        if product["id"].upper() == product_id.upper():
            return product
    return None


def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()

    if product_id == "":
        print("Error: Product ID cannot be empty.")
        return
    if find_product(inventory, product_id):
        print(f"Error: Product ID {product_id} already exists.")
        return

    name = input("Product Name: ").strip()
    if name == "":
        print("Error: Product name cannot be empty.")
        return

    price = get_positive_float("Price: ")
    stock = get_positive_int("Stock Quantity: ")

    inventory.append({
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock,
    })
    print("Product added successfully!")


def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = find_product(inventory, product_id)

    if product is None:
        print("Product not found.")
        return

    print(f"\nProduct Found: Name: {product['name']} Current Stock: {product['stock']}")
    product["stock"] = get_positive_int("New Stock Quantity: ")
    print("Stock updated successfully!")


def search_product(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = find_product(inventory, product_id)

    if product is None:
        print("Product not found.")
        return

    print("Product Found")
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")


def display_all(inventory):
    print("\nCurrent Inventory")
    if not inventory:
        print("Inventory is empty.")
        return
    for p in inventory:
        print(f"ID: {p['id']} | Name: {p['name']} | "
              f"Price: ${p['price']:.2f} | Stock: {p['stock']}")


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
    if not inventory:
        inventory = [
            {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
            {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
            {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25},
        ]
        print("Loaded 3 starter products.")

    while True:
        show_menu()
        choice = input("\nEnter option: ").strip()

        if choice == "1":
            display_all(inventory)
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
