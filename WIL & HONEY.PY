RESTURANT_NAME = "WIL & HONEY"

MENU = {
    "1" :  {
        "Name": "Sandwish", "Price": 5.00
    },

    "2" :  {
    "Name": " Hawaii Pizza", "Price": 10.00
    },


    "3" :  {
        "Name": " Corn Pizza", "Price": 7.00
    },


    "4" :  {
        "Name": " Pepperoni Pizza", "Price": 6.00
    },

    "5" :  {
        "Name": " Vegetable Pizza", "Price": 9.00
    },


    "6" :  {
        "Name": " Cheese Pizza", "Price": 7.50
    },

    "7" :  {
        "Name": "Jollof Rice", "Price": 5.50
    },

    "8" :  {
        "Name": " Dry Rice ", "Price": 10.00
    },

    "9" :  {
    "Name": "Ice Cream", "Price": 3.00
    },

    "10" :  {
        "Name": "French Fry", "Price": 2.50
    }

}

App_actions = {
    "1": "add a new menu to cart",
    "2": "Remove an item from cart",
    "3": "Modify a cart item's quantity",
    "4": "View cart",
    "5": "checkout",
    "6": "Exit",

}

SALES_TAX = 0.07
cart = {}

def display_menu():
    print("\n****Menu****\n")
    for sku in MENU: # Changed 'menu' to 'MENU'
        # Removed sku[3:] slicing as keys are now '1', '2', etc.
        item = MENU[sku]['Name'] # Changed 'menu' to 'MENU' and 'name' to 'Name'
        price = MENU[sku]['Price'] # Changed 'menu' to 'MENU' and 'price' to 'Price'
        print("("+ sku + ")" + " " + item + ": $" + str(price))
    print()
    
    display_menu()
    
def add_to_cart(sku, quantity=1):
    if sku in MENU:
        if sku in cart:
            # If item is already in cart, update its quantity
            cart[sku]['quantity'] += quantity
            print(f"Updated quantity for {MENU[sku]['Name']} to {cart[sku]['quantity']}.")
        else:
            # If item is new, add it to cart with its details
            cart[sku] = {
                'name': MENU[sku]['Name'],
                'price': MENU[sku]['Price'],
                'quantity': quantity
            }
            print("Added" , quantity,"of", MENU[sku]['Name'], "to the cart.")
    else:
        # Corrected f-string usage
        print(f"I'm sorry, The menu number {sku} that you entered is not in our menu.")

    add_to_cart("2", quantity=1)
    
def remove_from_cart(sku):
    if sku in cart:
        removed_val = cart.pop(sku)
        print(f"Removed {removed_val['name']} from the cart.")
    else:
        print(f"I'm sorry, The item SKU {sku} is not in our cart.")

def calculate_total():
    subtotal = 0
    for sku, item_details in cart.items():
        subtotal += item_details['price'] * item_details['quantity']

    tax_amount = subtotal * SALES_TAX
    total = subtotal + tax_amount

    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Sales Tax ({SALES_TAX*100:.0f}%): ${tax_amount:.2f}")
    print(f"Total: ${total:.2f}")
    return total

remove_from_cart("sku1")

calculate_total()

def view_cart():
    print("\n***** Cart Contents *****\n")
    subtotal = 0
    for sku in cart: # Iterate over SKUs (keys)
        item_details = cart[sku] # Get the dictionary for the item
        quantity = item_details['quantity']
        item_name = item_details['name']
        item_price = item_details['price']

        subtotal += item_price * quantity
        print(f"{quantity} x {item_name} (${item_price:.2f} each)")

    tax = subtotal * SALES_TAX # Corrected SALES_TAX_RATE to SALES_TAX
    total = subtotal + tax # Corrected aubtotal to subtotal

    print(f"\nSubtotal: ${subtotal:.2f}")
    print(f"Sales Tax ({SALES_TAX*100:.0f}%): ${tax:.2f}")
    print(f"Total: ${total:.2f}") # Corrected indentation and used f-string
    print("\n")
    
def process_refund(order_id):
    """Process a refund for a completed order"""
    global order_history
    
    if order_id not in order_history:
        print("Error: Order not found.")
        return False
    
    order = order_history[order_id]
    
    if order['status'] != 'completed':
        print("Error: This order is not eligible for refund.")
        return False
    
    # Check if refund is within 7 days of purchase
    purchase_date = datetime.strptime(order['date'], "%Y-%m-%d %H:%M:%S")
    current_date = datetime.now()
    days_since_purchase = (current_date - purchase_date).days
    
    if days_since_purchase > 7:
        print("Error: Refund can only be processed within 7 days of purchase.")
        return False
    
    # Process refund
    try:
        print("\nRefund Details:")
        print(f"Order ID: {order_id}")
        print(f"Refund Amount: ${order['total']:.2f}")
        print("\nItems being refunded:")
        
        for sku, item in order['items'].items():
            print(f"{item['quantity']} x {item['name']}")
        
        confirm = input("\nConfirm refund? (yes/no): ").lower()
        
        if confirm == 'yes':
            # Simulate refund processing
            refund_successful = process_refund_payment(order_id, order['total'])
            
            if refund_successful:
                order['status'] = 'refunded'
                print("\nRefund processed successfully!")
                print(f"Refund amount of ${order['total']:.2f} will be credited back to your original payment method.")
                return True
            else:
                print("\nRefund processing failed. Please try again or contact customer service.")
                return False
        else:
            print("Refund cancelled.")
            return False
            
    except Exception as e:
        print(f"Error processing refund: {e}")
        return False

def process_refund_payment(order_id, amount):
    """Simulate refund processing"""
    import random
    # Simulate random refund success/failure
    return random.choice([True, True, False])  # 66% success rate

def view_order_history():
    """Display all completed and refunded orders"""
    print("\n***** Order History *****\n")
    
    if not order_history:
        print("No orders found.")
        return
    
    for order_id, order in order_history.items():
        print(f"\nOrder ID: {order_id}")
        print(f"Date: {order['date']}")
        print(f"Status: {order['status']}")
        print(f"Payment Method: {'Credit Card' if order['payment_method'] == '1' else 'Cash'}")
        print("\nItems:")
        
        for sku, item in order['items'].items():
            print(f"{item['quantity']} x {item['name']} (${item['price']:.2f} each)")
        
        print(f"\nTotal: ${order['total']:.2f}")
    
    print("\n")
elif response == "6":
        print("\nWould you like to:")
        print("1. View order history")
        print("2. Request a refund")
        choice = input("Enter your choice (1-2): ")
        
        if choice == "1":
            view_order_history()
        elif choice == "2":
            order_id = input("Enter order ID for refund: ")
            process_refund(order_id)
    elif response == "7":
        print ("Goodbye!")
        ordering = False
SALES_TAX = 0.07
cart = {}
order_history = {}  # Format: {order_id: {'items': {...}, 'total': amount, 'status': 'completed/refunded'}}
next_order_id = 1

# Inventory system
inventory = {
    "1": {"Name": "Sandwish", "Price": 5.00, "Stock": 20},
    "2": {"Name": " Hawaii Pizza", "Price": 10.00, "Stock": 15},
    "3": {"Name": " Corn Pizza", "Price": 7.00, "Stock": 15},
    "4": {"Name": " Pepperoni Pizza", "Price": 6.00, "Stock": 15},
    "5": {"Name": " Vegetable Pizza", "Price": 9.00, "Stock": 15},
    "6": {"Name": " Cheese Pizza", "Price": 7.50, "Stock": 15},
    "7": {"Name": "Jollof Rice", "Price": 5.50, "Stock": 20},
    "8": {"Name": " Dry Rice ", "Price": 10.00, "Stock": 20},
    "9": {"Name": "Ice Cream", "Price": 3.00, "Stock": 25},
    "10": {"Name": "French Fry", "Price": 2.50, "Stock": 30}
}

# Low stock threshold
LOW_STOCK_THRESHOLD = 5
print("("+ sku + ")" + " " + item + ": $" + str(price) + " (Stock: " + str(inventory[sku]['Stock']) + ")")
def add_to_cart(sku, quantity=1):
    if sku in MENU:
        if sku not in inventory:
            print(f"Error: Item {sku} not found in inventory.")
            return False
            
        if inventory[sku]['Stock'] < quantity:
            print(f"Sorry, only {inventory[sku]['Stock']} units of {inventory[sku]['Name']} available.")
            return False
            
        if sku in cart:
            # If item is already in cart, update its quantity
            new_quantity = cart[sku]['quantity'] + quantity
            if new_quantity > inventory[sku]['Stock']:
                print(f"Sorry, cannot add more {inventory[sku]['Name']}. Only {inventory[sku]['Stock']} units available.")
                return False
                
            cart[sku]['quantity'] = new_quantity
            print(f"Updated quantity for {inventory[sku]['Name']} to {new_quantity}.")
        else:
            # If item is new, add it to cart with its details
            cart[sku] = {
                'name': inventory[sku]['Name'],
                'price': inventory[sku]['Price'],
                'quantity': quantity
            }
            print("Added" , quantity,"of", inventory[sku]['Name'], "to the cart.")
        
        # Update inventory
        inventory[sku]['Stock'] -= quantity
        
        # Check for low stock
        if inventory[sku]['Stock'] <= LOW_STOCK_THRESHOLD:
            print(f"Warning: Low stock for {inventory[sku]['Name']}. Only {inventory[sku]['Stock']} units remaining.")
        
        return True
    else:
        # Corrected f-string usage
        print(f"I'm sorry, The menu number {sku} that you entered is not in our menu.")
        return False
if payment_successful:
                    # Store order in history
                    order_id = f"ORD{next_order_id:04d}"
                    order_history[order_id] = {
                        'items': cart.copy(),
                        'total': total,
                        'status': 'completed',
                        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'payment_method': payment_method
                    }
                    next_order_id += 1
                    
                    print(f"\nPayment of ${total:.2f} processed successfully.")
                    print(f"Order ID: {order_id}")
                    print("Thank you for shopping with WIL & HONEY!!!!!")
                    # Clear cart after successful payment
                    cart.clear()
                    print("\nYour order has been placed successfully.")
                    return True
                else:
                    # Restore stock if payment fails
                    for sku, item in cart.items():
                        if sku in inventory:
                            inventory[sku]['Stock'] += item['quantity']
                    print("\nPayment failed. Your items have been restored to inventory.")
                    print("Please try again or contact customer service.")
                    return False
if payment_successful:
                    # Store order in history
                    order_id = f"ORD{next_order_id:04d}"
                    order_history[order_id] = {
                        'items': cart.copy(),
                        'total': total,
                        'status': 'completed',
                        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'payment_method': payment_method
                    }
                    next_order_id += 1
                    
                    print(f"\nPayment of ${total:.2f} processed successfully.")
                    print(f"Order ID: {order_id}")
                    print("Thank you for shopping with WIL & HONEY!!!!!")
                    # Clear cart after successful payment
                    cart.clear()
                    print("\nYour order has been placed successfully.")
                    return True
                else:
                    # Restore stock if payment fails
                    for sku, item in cart.items():
                        if sku in inventory:
                            inventory[sku]['Stock'] += item['quantity']
                    print("\nPayment failed. Your items have been restored to inventory.")
                    print("Please try again or contact customer service.")
                    return False
def restock_item(sku, quantity):
    """Add stock to an item in inventory"""
    if sku not in inventory:
        print(f"Error: Item {sku} not found in inventory.")
        return False
        
    if quantity <= 0:
        print("Error: Restock quantity must be positive.")
        return False
        
    inventory[sku]['Stock'] += quantity
    print(f"Added {quantity} units of {inventory[sku]['Name']}. Current stock: {inventory[sku]['Stock']}")
    
    # Check if item was previously low stock
    if inventory[sku]['Stock'] > LOW_STOCK_THRESHOLD:
        print(f"Stock for {inventory[sku]['Name']} is now sufficient.")
    
    return True

def view_inventory():
    """Display current inventory status"""
    print("\n***** Inventory Status *****\n")
    
    for sku in inventory:
        item = inventory[sku]
        stock_status = "LOW STOCK" if item['Stock'] <= LOW_STOCK_THRESHOLD else "In Stock"
        print(f"({sku}) {item['Name']}: ${item['Price']} - {item['Stock']} units ({stock_status})")
    
    print("\n")
def restock_item(sku, quantity):
    """Add stock to an item in inventory"""
    if sku not in inventory:
        print(f"Error: Item {sku} not found in inventory.")
        return False
        
    if quantity <= 0:
        print("Error: Restock quantity must be positive.")
        return False
        
    inventory[sku]['Stock'] += quantity
    print(f"Added {quantity} units of {inventory[sku]['Name']}. Current stock: {inventory[sku]['Stock']}")
    
    # Check if item was previously low stock
    if inventory[sku]['Stock'] > LOW_STOCK_THRESHOLD:
        print(f"Stock for {inventory[sku]['Name']} is now sufficient.")
    
    return True

def view_inventory():
    """Display current inventory status"""
    print("\n***** Inventory Status *****\n")
    
    for sku in inventory:
        item = inventory[sku]
        stock_status = "LOW STOCK" if item['Stock'] <= LOW_STOCK_THRESHOLD else "In Stock"
        print(f"({sku}) {item['Name']}: ${item['Price']} - {item['Stock']} units ({stock_status})")
    
    print("\n")
elif response == "6":
        print("\nWould you like to:")
        print("1. View order history")
        print("2. Request a refund")
        print("3. View inventory")
        print("4. Restock item")
        choice = input("Enter your choice (1-4): ")
        
        if choice == "1":
            view_order_history()
        elif choice == "2":
            order_id = input("Enter order ID for refund: ")
            process_refund(order_id)
        elif choice == "3":
            view_inventory()
        elif choice == "4":
            sku = input("Enter item SKU to restock: ")
            try:
                quantity = int(input("Enter quantity to add: "))
                restock_item(sku, quantity)
            except ValueError:
                print("Error: Invalid quantity entered.")
    elif response == "7":
        print ("Goodbye!")
        ordering = False
stock = inventory[sku]['Stock']
        if stock == 0:
            print("("+ sku + ")" + " " + item + ": $" + str(price) + " - OUT OF STOCK")
        else:
            print("("+ sku + ")" + " " + item + ": $" + str(price) + " (Stock: " + str(stock) + ")")
stock = inventory[sku]['Stock']
        if stock == 0:
            print("("+ sku + ")" + " " + item + ": $" + str(price) + " - OUT OF STOCK")
        else:
            print("("+ sku + ")" + " " + item + ": $" + str(price) + " (Stock: " + str(stock) + ")")
stock = inventory[sku]['Stock']
        if stock == 0:
            print("("+ sku + ")" + " " + item + ": $" + str(price) + " - OUT OF STOCK")
        else:
            print("("+ sku + ")" + " " + item + ": $" + str(price) + " (Stock: " + str(stock) + ")")
def add_to_cart(sku, quantity=1):
    if sku in MENU:
        if sku not in inventory:
            print(f"Error: Item {sku} not found in inventory.")
            return False
            
        if inventory[sku]['Stock'] == 0:
            print(f"Sorry, {inventory[sku]['Name']} is currently out of stock.")
            print("Would you like to:")
            print("1. Choose a different item")
            print("2. View similar items")
            choice = input("Enter your choice (1-2): ")
            
            if choice == "1":
                return False
            elif choice == "2":
                show_similar_items(sku)
                return False
            else:
                print("Invalid choice. Please try again.")
                return False
            
        if quantity > inventory[sku]['Stock']:
            print(f"Sorry, we only have {inventory[sku]['Stock']} units of {inventory[sku]['Name']} available.")
            print("Would you like to:")
            print("1. Add available quantity to cart")
            print("2. Choose a different quantity")
            print("3. Choose a different item")
            choice = input("Enter your choice (1-3): ")
            
            if choice == "1":
                quantity = inventory[sku]['Stock']
            elif choice == "2":
                try:
                    new_quantity = int(input("Enter new quantity: "))
                    if new_quantity <= 0:
                        print("Quantity must be positive.")
                        return False
                    if new_quantity > inventory[sku]['Stock']:
                        print("Requested quantity exceeds available stock.")
                        return False
                    quantity = new_quantity
                except ValueError:
                    print("Invalid quantity entered.")
                    return False
            elif choice == "3":
                return False
            else:
                print("Invalid choice. Please try again.")
                return False
            
        if sku in cart:
            # If item is already in cart, update its quantity
            new_quantity = cart[sku]['quantity'] + quantity
            if new_quantity > inventory[sku]['Stock']:
                print(f"Sorry, cannot add more {inventory[sku]['Name']}. Only {inventory[sku]['Stock']} units available.")
                return False
                
            cart[sku]['quantity'] = new_quantity
            print(f"Updated quantity for {inventory[sku]['Name']} to {new_quantity}.")
        else:
            # If item is new, add it to cart with its details
            cart[sku] = {
                'name': inventory[sku]['Name'],
                'price': inventory[sku]['Price'],
                'quantity': quantity
            }
            print("Added" , quantity,"of", inventory[sku]['Name'], "to the cart.")
        
        # Update inventory
        inventory[sku]['Stock'] -= quantity
        
        # Check for low stock
        if inventory[sku]['Stock'] <= LOW_STOCK_THRESHOLD:
            print(f"Warning: Low stock for {inventory[sku]['Name']}. Only {inventory[sku]['Stock']} units remaining.")
        
        return True
    else:
        # Corrected f-string usage
        print(f"I'm sorry, The menu number {sku} that you entered is not in our menu.")
        return False
def add_to_cart(sku, quantity=1):
    if sku in MENU:
        if sku not in inventory:
            print(f"Error: Item {sku} not found in inventory.")
            return False
            
        if inventory[sku]['Stock'] == 0:
            print(f"Sorry, {inventory[sku]['Name']} is currently out of stock.")
            print("Would you like to:")
            print("1. Choose a different item")
            print("2. View similar items")
            choice = input("Enter your choice (1-2): ")
            
            if choice == "1":
                return False
            elif choice == "2":
                show_similar_items(sku)
                return False
            else:
                print("Invalid choice. Please try again.")
                return False
            
        if quantity > inventory[sku]['Stock']:
            print(f"Sorry, we only have {inventory[sku]['Stock']} units of {inventory[sku]['Name']} available.")
            print("Would you like to:")
            print("1. Add available quantity to cart")
            print("2. Choose a different quantity")
            print("3. Choose a different item")
            choice = input("Enter your choice (1-3): ")
            
            if choice == "1":
                quantity = inventory[sku]['Stock']
            elif choice == "2":
                try:
                    new_quantity = int(input("Enter new quantity: "))
                    if new_quantity <= 0:
                        print("Quantity must be positive.")
                        return False
                    if new_quantity > inventory[sku]['Stock']:
                        print("Requested quantity exceeds available stock.")
                        return False
                    quantity = new_quantity
                except ValueError:
                    print("Invalid quantity entered.")
                    return False
            elif choice == "3":
                return False
            else:
                print("Invalid choice. Please try again.")
                return False
            
        if sku in cart:
            # If item is already in cart, update its quantity
            new_quantity = cart[sku]['quantity'] + quantity
            if new_quantity > inventory[sku]['Stock']:
                print(f"Sorry, cannot add more {inventory[sku]['Name']}. Only {inventory[sku]['Stock']} units available.")
                return False
                
            cart[sku]['quantity'] = new_quantity
            print(f"Updated quantity for {inventory[sku]['Name']} to {new_quantity}.")
        else:
            # If item is new, add it to cart with its details
            cart[sku] = {
                'name': inventory[sku]['Name'],
                'price': inventory[sku]['Price'],
                'quantity': quantity
            }
            print("Added" , quantity,"of", inventory[sku]['Name'], "to the cart.")
        
        # Update inventory
        inventory[sku]['Stock'] -= quantity
        
        # Check for low stock
        if inventory[sku]['Stock'] <= LOW_STOCK_THRESHOLD:
            print(f"Warning: Low stock for {inventory[sku]['Name']}. Only {inventory[sku]['Stock']} units remaining.")
        
        return True
    else:
        # Corrected f-string usage
        print(f"I'm sorry, The menu number {sku} that you entered is not in our menu.")
        return False
def add_to_cart(sku, quantity=1):
    if sku in MENU:
        if sku not in inventory:
            print(f"Error: Item {sku} not found in inventory.")
            return False
            
        if inventory[sku]['Stock'] == 0:
            print(f"Sorry, {inventory[sku]['Name']} is currently out of stock.")
            print("Would you like to:")
            print("1. Choose a different item")
            print("2. View similar items")
            choice = input("Enter your choice (1-2): ")
            
            if choice == "1":
                return False
            elif choice == "2":
                show_similar_items(sku)
                return False
            else:
                print("Invalid choice. Please try again.")
                return False
            
        if quantity > inventory[sku]['Stock']:
            print(f"Sorry, we only have {inventory[sku]['Stock']} units of {inventory[sku]['Name']} available.")
            print("Would you like to:")
            print("1. Add available quantity to cart")
            print("2. Choose a different quantity")
            print("3. Choose a different item")
            choice = input("Enter your choice (1-3): ")
            
            if choice == "1":
                quantity = inventory[sku]['Stock']
            elif choice == "2":
                try:
                    new_quantity = int(input("Enter new quantity: "))
                    if new_quantity <= 0:
                        print("Quantity must be positive.")
                        return False
                    if new_quantity > inventory[sku]['Stock']:
                        print("Requested quantity exceeds available stock.")
                        return False
                    quantity = new_quantity
                except ValueError:
                    print("Invalid quantity entered.")
                    return False
            elif choice == "3":
                return False
            else:
                print("Invalid choice. Please try again.")
                return False
            
        if sku in cart:
            # If item is already in cart, update its quantity
            new_quantity = cart[sku]['quantity'] + quantity
            if new_quantity > inventory[sku]['Stock']:
                print(f"Sorry, cannot add more {inventory[sku]['Name']}. Only {inventory[sku]['Stock']} units available.")
                return False
                
            cart[sku]['quantity'] = new_quantity
            print(f"Updated quantity for {inventory[sku]['Name']} to {new_quantity}.")
        else:
            # If item is new, add it to cart with its details
            cart[sku] = {
                'name': inventory[sku]['Name'],
                'price': inventory[sku]['Price'],
                'quantity': quantity
            }
            print("Added" , quantity,"of", inventory[sku]['Name'], "to the cart.")
        
        # Update inventory
        inventory[sku]['Stock'] -= quantity
        
        # Check for low stock
        if inventory[sku]['Stock'] <= LOW_STOCK_THRESHOLD:
            print(f"Warning: Low stock for {inventory[sku]['Name']}. Only {inventory[sku]['Stock']} units remaining.")
        
        return True
    else:
        # Corrected f-string usage
        print(f"I'm sorry, The menu number {sku} that you entered is not in our menu.")
        return False
def add_to_cart(sku, quantity=1):
    if sku in MENU:
        if sku not in inventory:
            print(f"Error: Item {sku} not found in inventory.")
            return False
            
        if inventory[sku]['Stock'] == 0:
            print(f"Sorry, {inventory[sku]['Name']} is currently out of stock.")
            print("Would you like to:")
            print("1. Choose a different item")
            print("2. View similar items")
            choice = input("Enter your choice (1-2): ")
            
            if choice == "1":
                return False
            elif choice == "2":
                show_similar_items(sku)
                return False
            else:
                print("Invalid choice. Please try again.")
                return False
            
        if quantity > inventory[sku]['Stock']:
            print(f"Sorry, we only have {inventory[sku]['Stock']} units of {inventory[sku]['Name']} available.")
            print("Would you like to:")
            print("1. Add available quantity to cart")
            print("2. Choose a different quantity")
            print("3. Choose a different item")
            choice = input("Enter your choice (1-3): ")
            
            if choice == "1":
                quantity = inventory[sku]['Stock']
            elif choice == "2":
                try:
                    new_quantity = int(input("Enter new quantity: "))
                    if new_quantity <= 0:
                        print("Quantity must be positive.")
                        return False
                    if new_quantity > inventory[sku]['Stock']:
                        print("Requested quantity exceeds available stock.")
                        return False
                    quantity = new_quantity
                except ValueError:
                    print("Invalid quantity entered.")
                    return False
            elif choice == "3":
                return False
            else:
                print("Invalid choice. Please try again.")
                return False
            
        if sku in cart:
            # If item is already in cart, update its quantity
            new_quantity = cart[sku]['quantity'] + quantity
            if new_quantity > inventory[sku]['Stock']:
                print(f"Sorry, cannot add more {inventory[sku]['Name']}. Only {inventory[sku]['Stock']} units available.")
                return False
                
            cart[sku]['quantity'] = new_quantity
            print(f"Updated quantity for {inventory[sku]['Name']} to {new_quantity}.")
        else:
            # If item is new, add it to cart with its details
            cart[sku] = {
                'name': inventory[sku]['Name'],
                'price': inventory[sku]['Price'],
                'quantity': quantity
            }
            print("Added" , quantity,"of", inventory[sku]['Name'], "to the cart.")
        
        # Update inventory
        inventory[sku]['Stock'] -= quantity
        
        # Check for low stock
        if inventory[sku]['Stock'] <= LOW_STOCK_THRESHOLD:
            print(f"Warning: Low stock for {inventory[sku]['Name']}. Only {inventory[sku]['Stock']} units remaining.")
        
        return True
    else:
        # Corrected f-string usage
        print(f"I'm sorry, The menu number {sku} that you entered is not in our menu.")
        return False
def show_similar_items(sku):
    """Show similar items when an item is out of stock"""
    current_item = inventory[sku]
    print("\nSimilar items might be available:")
    
    for other_sku, other_item in inventory.items():
        if other_sku != sku and other_item['Stock'] > 0:
            # Check if items are similar by name or category
            if (current_item['Name'].split()[0] == other_item['Name'].split()[0] or
                current_item['Name'].split()[-1] == other_item['Name().split()[-1]]):
                print(f"({other_sku}) {other_item['Name']}: ${other_item['Price']} (Stock: {other_item['Stock']})")
    
    print("\n")
def show_similar_items(sku):
    """Show similar items when an item is out of stock"""
    current_item = inventory[sku]
    print("\nSimilar items might be available:")
    
    for other_sku, other_item in inventory.items():
        if other_sku != sku and other_item['Stock'] > 0:
            # Check if items are similar by name or category
            if (current_item['Name'].split()[0] == other_item['Name'].split()[0] or
                current_item['Name'].split()[-1] == other_item['Name().split()[-1]]):
                print(f"({other_sku}) {other_item['Name']}: ${other_item['Price']} (Stock: {other_item['Stock']})")
    
    print("\n")
def show_similar_items(sku):
    """Show similar items when an item is out of stock"""
    current_item = inventory[sku]
    print("\nSimilar items might be available:")
    
    for other_sku, other_item in inventory.items():
        if other_sku != sku and other_item['Stock'] > 0:
            # Check if items are similar by name or category
            if (current_item['Name'].split()[0] == other_item['Name'].split()[0] or
                current_item['Name'].split()[-1] == other_item['Name().split()[-1]]):
                print(f"({other_sku}) {other_item['Name']}: ${other_item['Price']} (Stock: {other_item['Stock']})")
    
    print("\n")
def notify_stock_available(sku):
    """Notify user when an out-of-stock item becomes available"""
    if sku in inventory and inventory[sku]['Stock'] > 0:
        print(f"\nGood news! {inventory[sku]['Name']} is now available!")
        print(f"Current stock: {inventory[sku]['Stock']}")
        print("Would you like to add it to your cart? (yes/no)")
        choice = input().lower()
        
        if choice == 'yes':
            add_to_cart(sku)
        return True
    return False

def check_out_of_stock_items():
    """Check for any out-of-stock items and notify if they become available"""
    for sku, item in inventory.items():
        if item['Stock'] == 0:
            print(f"Currently out of stock: {item['Name']}")
            print("Would you like to be notified when it becomes available? (yes/no)")
            choice = input().lower()
            
            if choice == 'yes':
                # In a real system, this would add the user to a notification list
                print(f"You will be notified when {item['Name']} becomes available.")
def notify_stock_available(sku):
    """Notify user when an out-of-stock item becomes available"""
    if sku in inventory and inventory[sku]['Stock'] > 0:
        print(f"\nGood news! {inventory[sku]['Name']} is now available!")
        print(f"Current stock: {inventory[sku]['Stock']}")
        print("Would you like to add it to your cart? (yes/no)")
        choice = input().lower()
        
        if choice == 'yes':
            add_to_cart(sku)
        return True
    return False

def check_out_of_stock_items():
    """Check for any out-of-stock items and notify if they become available"""
    for sku, item in inventory.items():
        if item['Stock'] == 0:
            print(f"Currently out of stock: {item['Name']}")
            print("Would you like to be notified when it becomes available? (yes/no)")
            choice = input().lower()
            
            if choice == 'yes':
                # In a real system, this would add the user to a notification list
                print(f"You will be notified when {item['Name']} becomes available.")
elif response == "6":
        print("\nWould you like to:")
        print("1. View order history")
        print("2. Request a refund")
        print("3. View inventory")
        print("4. Restock item")
        print("5. Check out-of-stock items")
        choice = input("Enter your choice (1-5): ")
        
        if choice == "1":
            view_order_history()
        elif choice == "2":
            order_id = input("Enter order ID for refund: ")
            process_refund(order_id)
        elif choice == "3":
            view_inventory()
        elif choice == "4":
            sku = input("Enter item SKU to restock: ")
            try:
                quantity = int(input("Enter quantity to add: "))
                restock_item(sku, quantity)
            except ValueError:
                print("Error: Invalid quantity entered.")
        elif choice == "5":
            check_out_of_stock_items()
    elif response == "7":
        print ("Goodbye!")
        ordering = False
elif response == "6":
        print("\nWould you like to:")
        print("1. View order history")
        print("2. Request a refund")
        print("3. View inventory")
        print("4. Restock item")
        print("5. Check out-of-stock items")
        choice = input("Enter your choice (1-5): ")
        
        if choice == "1":
            view_order_history()
        elif choice == "2":
            order_id = input("Enter order ID for refund: ")
            process_refund(order_id)
        elif choice == "3":
            view_inventory()
        elif choice == "4":
            sku = input("Enter item SKU to restock: ")
            try:
                quantity = int(input("Enter quantity to add: "))
                restock_item(sku, quantity)
            except ValueError:
                print("Error: Invalid quantity entered.")
        elif choice == "5":
            check_out_of_stock_items()
    elif response == "7":
        print ("Goodbye!")
        ordering = False

def checkout():
    print("\n****Checkout****\n")
    
    # Check if cart is empty
    if not cart:
        print("Your cart is empty. Please add items before checkout.")
        return
    
    # Display cart contents
    view_cart()
    
    # Payment processing
    print("\nPlease select your payment method:")
    print("1. Credit Card")
    print("2. Cash")
    payment_method = input("Enter your choice (1 or 2): ")
    
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Validate payment method
            if payment_method not in ["1", "2"]:
                raise ValueError("Invalid payment method selected.")
            
            # Get payment details
            if payment_method == "1":
                card_number = input("Enter your credit card number: ")
                if len(card_number) != 16 or not card_number.isdigit():
                    raise ValueError("Invalid credit card number.")
                expiry_date = input("Enter expiry date (MM/YY): ")
                cvv = input("Enter CVV: ")
                if len(cvv) != 3 or not cvv.isdigit():
                    raise ValueError("Invalid CVV.")
            
            # Calculate total
            total = calculate_total()
            
            # Confirm transaction
            print("\nPlease confirm your transaction:")
            confirm = input("Enter 'yes' to confirm or 'no' to cancel: ").lower()
            
            if confirm == 'yes':
                # Simulate payment processing
                payment_successful = process_payment(payment_method, total)
                
                if payment_successful:
                    print(f"\nPayment of ${total:.2f} processed successfully.")
                    print("Thank you for shopping with WIL & HONEY!!!!!")
                    # Clear cart after successful payment
                    cart.clear()
                    print("\nYour order has been placed successfully.")
                    return
                else:
                    print("\nPayment failed. Please try again.")
                    retry_count += 1
                    if retry_count < max_retries:
                        print(f"You have {max_retries - retry_count} attempts remaining.")
                        print("\nWould you like to:")
                        print("1. Try payment again")
                        print("2. Change payment method")
                        print("3. Cancel checkout")
                        choice = input("Enter your choice (1-3): ")
                        
                        if choice == "1":
                            continue
                        elif choice == "2":
                            payment_method = input("Enter your choice (1 or 2): ")
                            continue
                        else:
                            print("Transaction cancelled.")
                            return
                    else:
                        print("Maximum retry attempts reached. Please try again later.")
                        return
            else:
                print("Transaction cancelled.")
                return
                
        except ValueError as e:
            print(f"Error: {e}")
            retry_count += 1
            if retry_count < max_retries:
                print(f"You have {max_retries - retry_count} attempts remaining.")
                continue
            else:
                print("Maximum retry attempts reached. Please try again later.")
                return
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Please contact customer service.")
            return

def process_payment(method, amount):
    """Simulate payment processing"""
    import random
    # Simulate random payment success/failure
    return random.choice([True, True, False])  # 66% success rate


def get_sku_and_quantity(sku_prompt, quantity_prompt=None):
    item_sku = input(sku_prompt)
    quantity = 1
    if quantity_prompt:
        try:
            quantity = int(input(quantity_prompt))
        except ValueError:
            print("Invalid quantity. Defaulting to 1.")
            quantity = 1 # Default to 1 if input is not an integer
    return item_sku, quantity

def order_loop():
  print(f"Welcome to {RESTURANT_NAME}!")
  ordering = True
  print("\n*****Ordering Actions****\n")
  while ordering:
    for action in App_actions:
      description = App_actions[action]
      print(f"({action}) {description}")
    print()

    response = input("Please select an action: ")
    if response == "1":
      display_menu()
      sku_prompt = "Please enter the SKU number for the menu item you want to order: "
      quantity_prompt = "Please enter the quantity you want to order [default is 1]:"
      ordered_sku, order_quantity = get_sku_and_quantity(sku_prompt, quantity_prompt)
      add_to_cart(ordered_sku, order_quantity)
    elif response == "2":
      display_menu()
      sku_prompt = "Please enter the SKU number for the menu item you want to remove: "
      item_sku_to_remove = get_sku_and_quantity(sku_prompt)
      remove_from_cart(item_sku_to_remove)
    elif response == "3":
      modify_cart()
    elif response == "4":
      view_cart()
    elif response == "5":
      checkout()
      ordering = False
    elif response == "6":
      print ("Goodbye!")
      ordering = False
    else:
      print("You have entered an invalid action number. Please try again ")


def modify_cart():
    view_cart()
    sku_prompt = "Please enter the SKU number for the menu item you want to modify: "
    quantity_prompt = "Please enter the new quantity: "
    item_sku, new_quantity = get_sku_and_quantity(sku_prompt, quantity_prompt)
    if item_sku in cart:
        if new_quantity > 0:
            cart[item_sku]['quantity'] = new_quantity
            print(f"Updated quantity for {cart[item_sku]['name']} to {new_quantity}.")
        else:
            remove_from_cart(item_sku)
    else:
        print(f"I'm sorry, The item SKU {item_sku} is not in our cart.")


def modify_cart():
  print("\n**** Modify Cart ****\n")
  view_cart()
  if not cart:
    print("Your cart is empty. Nothing to modify.")
    return

  sku_to_modify = get_sku_and_quantity("Enter the SKU of the item you want to modify: ")

  if sku_to_modify in cart:
    try:
      new_quantity = int(input(f"Enter new quantity for {cart[sku_to_modify]['name']} (current: {cart[sku_to_modify]['quantity']}): "))
      if new_quantity <= 0:
        item_name_removed = cart[sku_to_modify]['name'] # Get name before removing
        remove_from_cart(sku_to_modify)
        print(f"Removed {item_name_removed} from cart as quantity was set to {new_quantity}.")
      else:
        cart[sku_to_modify]['quantity'] = new_quantity
        print(f"Updated {cart[sku_to_modify]['name']} quantity to {new_quantity}.")
    except ValueError:
      print("Invalid quantity entered. Please enter a number.")
  else:
    print(f"Item with SKU '{sku_to_modify}' not found in your cart.")

order_loop()

