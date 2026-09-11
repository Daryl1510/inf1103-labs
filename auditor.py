def main():
    total_inventory = 0        
    total_units_processed = 0
    failed_entries = 0

    while True:               
        entry = input("Enter stock quantity (or 'quit' to finish): ").strip()

        if entry.lower() == "quit":
            break

        if not entry.isdigit():
            print(f"Error: '{entry}' is not a valid number. Entry rejected.")
            failed_entries += 1
            continue

        quantity = int(entry)  

        if quantity < 0:
            print(f"Error: {quantity} is negative. Entry rejected.")
            failed_entries += 1
            continue

        total_inventory += quantity
        total_units_processed += quantity
        print(f"Accepted {quantity} units. Current inventory: {total_inventory}")

      
        if total_inventory > 500:
            print(f"OVERSTOCK ALERT: Inventory ({total_inventory}) exceeds 500 units!")
            break
        elif total_inventory == 500:
            print("Inventory has reached maximum capacity (500 units).")
        else:
            pass  

    print("\n--- Inventory Audit Report ---")
    print(f"Total Units Processed: {total_units_processed}")
    print(f"Number of Failed/Rejected Entries: {failed_entries}")



if __name__ == "__main__":
    main()