TAX_RATE = 0.10
OVERSTOCK_LIMIT = 500
INVENTORY_FILE = "inventory.txt"


def load_inventory():
    """
    Reads the saved total and transaction history from INVENTORY_FILE.
    If the file doesn't exist yet (first-ever run), start clean instead
    of crashing.
    Returns a tuple: (total_inventory, history_list)
    """
    try:
        with open(INVENTORY_FILE, "r") as file:
            lines = file.readlines()

        total_inventory = 0
        history = []

        for line in lines:
            line = line.strip()
            if line.startswith("TOTAL="):
                total_inventory = int(line.replace("TOTAL=", ""))
            elif line.startswith("HISTORY="):
                raw_history = line.replace("HISTORY=", "")
                if raw_history:  # avoid turning "" into [0]
                    history = [int(x) for x in raw_history.split(",")]

        print(f"Loaded saved inventory: {total_inventory} units, "
              f"{len(history)} past transaction(s).")
        return total_inventory, history

    except FileNotFoundError:
        print("No previous inventory file found. Starting fresh.")
        return 0, []


def save_inventory(total_inventory, history):
    """
    Writes the current total and the full transaction history back to
    INVENTORY_FILE so the data survives after the program closes.
    """
    with open(INVENTORY_FILE, "w") as file:
        file.write(f"TOTAL={total_inventory}\n")
        file.write("HISTORY=" + ",".join(str(h) for h in history) + "\n")

    print(f"Inventory successfully saved to {INVENTORY_FILE}.")


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


def generate_report(total_units, failed_attempts, history):
    print("\n--- Inventory Audit Report ---")
    print(f"Total Units Processed This Session: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")
    print(f"Full Transaction History: {history}")


def main():
    # --- Persistence: load whatever was saved last time ---
    total_inventory, history = load_inventory()

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

        # --- History Tracking: record every accepted transaction ---
        history.append(quantity)

        print(f"Accepted {quantity} units. Current inventory: {total_inventory}. "
              f"Tax on this delivery: {tax_owed:.2f}")

        if total_inventory > OVERSTOCK_LIMIT:
            print(f"OVERSTOCK ALERT: Inventory ({total_inventory}) exceeds {OVERSTOCK_LIMIT} units!")
            break
        elif total_inventory == OVERSTOCK_LIMIT:
            print(f"Inventory has reached maximum capacity ({OVERSTOCK_LIMIT} units).")

    generate_report(total_units_processed, failed_entries, history)

    # --- Write-Back: save the final total + history on quit ---
    save_inventory(total_inventory, history)


if __name__ == "__main__":
    main()