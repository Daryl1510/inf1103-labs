import csv

from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Read products from a CSV file, create each through ProductFactory and add it
    to the inventory.

    - A missing file is reported simply, without crashing (FileNotFoundError).
    - A bad row (unknown type, price that is not a number, negative stock, ...) is
      reported and skipped, and loading carries on (ValueError, per row).
    - finally always prints that the attempt is over, whatever happened.

    Expected columns: product_type,product_id,name,price,stock_quantity
    """
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)                         # skip the header row
            for line_number, row in enumerate(reader, start=2):
                if not row:                            # ignore blank lines
                    continue
                try:
                    product_type, product_id, name, price, stock_quantity = (
                        field.strip() for field in row)   # wrong column count -> ValueError
                    product = ProductFactory.create(product_type, product_id, name,
                                                    float(price), int(stock_quantity),
                                                    supplier)
                    if inventory.add_product(product):
                        loaded += 1
                    else:
                        print(f"Skipping row {line_number}: ID {product_id} already exists.")
                except ValueError as error:
                    print(f"Skipping row {line_number}: {error}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
