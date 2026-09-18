TAX_RATE = 0.10
OVERSTOCK_LIMIT = 500


def get_valid_input():

    entry = input("Enter stock quantity (or 'quit' to finish): ").strip()

    if entry.lower() == "quit":
        return "quit"

    if not entry.isdigit():
        print(f"Error: '{entry}' is not a valid number. Entry rejected.")
        return None

    quantity = int(entry)

    if quantity < 0:
        print(f"Error: {quantity} is negative. Entry rejected.")
        return None

    return quantity



def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * TAX_RATE


def generate_report(total_units, failed_attempts):
    print("\n--- Inventory Audit Report ---")
    print(f"Total Units Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


def main():
    total_inventory = 0
    total_units_processed = 0
    failed_entries = 0

    while True:
        result = get_valid_input()

        if result == "quit":
            break

        if result is None:
            failed_entries += 1
            continue


        quantity = result
        total_inventory = process_delivery(total_inventory, quantity)
        tax_owed = calculate_tax(quantity)
        total_units_processed += quantity

        print(f"Accepted {quantity} units. Current inventory: {total_inventory}. "
              f"Tax on this delivery: {tax_owed:.2f}")

        if total_inventory > OVERSTOCK_LIMIT:
            print(f"OVERSTOCK ALERT: Inventory ({total_inventory}) exceeds {OVERSTOCK_LIMIT} units!")
            break
        elif total_inventory == OVERSTOCK_LIMIT:
            print(f"Inventory has reached maximum capacity ({OVERSTOCK_LIMIT} units).")

    generate_report(total_units_processed, failed_entries)




if __name__ == "__main__":
    main()