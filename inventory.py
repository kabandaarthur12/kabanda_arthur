# Inventory management system
inventory = [
    {"name": "Keyboard", "quantity": 20, "price": 250},
    {"name": "Mouse", "quantity": 10, "price": 100},
    {"name": "Usb", "quantity": 30, "price": 50},
    {"name": "Calculator", "quantity": 40, "price": 190},
    {"name": "Monitor", "quantity": 60, "price": 500},
]

# Display items
def show_inventory():
    print("\n ---INVENTORY ITEMS---")
    print("\n Item Name   | Quantity | Price")
    print("-" * 35) 
    for item in inventory:
        print(f"{item['name']:<12} | {item['quantity']:<9} | ${item['price']}")
    print()   

# Add new item function
def add_item():
    print("\n--- ADD NEW ITEM ---")
    name = input("Enter item name: ")
    quantity = int(input("Enter quantity: "))
    price = float(input("Enter price: "))
    
    new_item = {"name": name, "quantity": quantity, "price": price}
    inventory.append(new_item)
    print(f"Added {name} to inventory successfully!")

# Update item function
def update_item():
    print("\n--- UPDATE ITEM ---")
    item_name = input("Enter item name to update: ")
    
    for item in inventory:
        if item['name'].lower() == item_name.lower():
            print(f"Current details - Quantity: {item['quantity']}, Price: ${item['price']}")
            item['quantity'] = int(input("Enter new quantity: "))
            item['price'] = float(input("Enter new price: "))
            print(f"Updated {item['name']} successfully!")
            return
    
    print("Item not found!")

# Remove item function
def remove_item():
    print("\n--- REMOVE ITEM ---")
    item_name = input("Enter item name to remove: ")
    
    for i, item in enumerate(inventory):
        if item['name'].lower() == item_name.lower():
            removed_item = inventory.pop(i)
            print(f"Removed {removed_item['name']} from inventory!")
            return
    
    print("Item not found!")

# Show main content
def main():
    while True:
        print("\n" + "="*50)
        print(" INVENTORY MANAGEMENT SYSTEM ")
        print("="*50)
        print("1. Show items in the inventory")
        print("2. Add a new item to inventory")
        print("3. Update item in inventory")
        print("4. Remove item from inventory")
        print("5. Exit")
        print("-" * 50)
        
        choice = input("Choose between 1-5: ").strip()
        
        if choice == "1":
            show_inventory()
        elif choice == "2":
            add_item()
        elif choice == "3":
            update_item()
        elif choice == "4":
            remove_item()
        elif choice == "5":
            print("Thank you for using this inventory management system!")
            break
        elif choice == "":
            print("Please enter a choice (1-5)")
        else:
            print(f"Invalid Choice '{choice}'! Please choose 1-5.")
            input("Press Enter to continue...")

# Run the program
if __name__ == "__main__":
    main()
