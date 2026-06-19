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
for sku in MENU:
     # Minimum stock levels for automated reordering
MINIMUM_STOCK_LEVELS = {
    "1": 10,
    "2": 10,
    "3": 10,
    "4": 10,
    "5": 10,
    "6": 10,
    "7": 10,
    "8": 10,
    "9": 15,
    "10": 15
}

# Supplier information for automated orders
AUTOMATED_ORDER_SUPPLIER = "FRESH_FOODS"
def check_restock_needed():
    """Check which items need to be restocked"""
    items_to_restock = []
    
    print("\n***** Items Needing Restock *****\n")
    
    for sku, item in inventory.items():
        if item['Stock'] <= MINIMUM_STOCK_LEVELS[sku]:
            needed = MINIMUM_STOCK_LEVELS[sku] - item['Stock']
            items_to_restock.append((sku, needed))
            print(f"{item['Name']}: Current stock {item['Stock']}, Need {needed} more units")
    
    if items_to_restock:
        print("\nWould you like to:")
        print("1. Create automated supplier order")
        print("2. Cancel")
        choice = input("Enter your choice (1-2): ")
        
        if choice == "1":
            create_automated_order(items_to_restock)
        else:
            print("No order created.")
    else:
        print("All items are sufficiently stocked.")
    
    return items_to_restock
def create_automated_order(items_to_restock):
    """Create an automated supplier order for restocking"""
    global next_supplier_order_id
    
    print("\n***** Creating Automated Supplier Order *****\n")
    
    order_id = f"SO{next_supplier_order_id:04d}"
    supplier_orders[order_id] = {
        'supplier': AUTOMATED_ORDER_SUPPLIER,
        'items': {},
        'status': 'pending',
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'expected_delivery': (datetime.now() + timedelta(days=suppliers[AUTOMATED_ORDER_SUPPLIER]['lead_time'])).strftime("%Y-%m-%d"),
        'automated': True
    }
    
    # Add items to order
    total_order_value = 0
    for sku, needed in items_to_restock:
        order_quantity = needed
        supplier_orders[order_id]['items'][sku] = order_quantity
        item_total = inventory[sku]['Price'] * order_quantity
        total_order_value += item_total
        print(f"Added {order_quantity} units of {inventory[sku]['Name']} to order")
    
    supplier_orders[order_id]['total'] = total_order_value
    
    print(f"\nAutomated order created:")
    print(f"Order ID: {order_id}")
    print(f"Supplier: {suppliers[AUTOMATED_ORDER_SUPPLIER]['name']}")
    print(f"Expected delivery: {supplier_orders[order_id]['expected_delivery']}")
    print(f"Order total: ${total_order_value:.2f}")
    
    next_supplier_order_id += 1
    return order_id
def schedule_restock_check():
    """Schedule automated restock checks"""
    import time
    
    print("\nScheduling automated restock checks...")
    print("Press Ctrl+C to stop automated checks")
    
    try:
        while True:
            print("\nRunning automated restock check...")
            check_restock_needed()
            print("\nNext check in 24 hours...")
            time.sleep(86400)  # 24 hours in seconds
    except KeyboardInterrupt:
        print("\nAutomated checks stopped by user.")
elif response == "6":
        print("\nWould you like to:")
        print("1. View order history")
        print("2. Request a refund")
        print("3. View inventory")
        print("4. Restock item")
        print("5. Check out-of-stock items")
        print("6. Create supplier order")
        print("7. Update supplier order status")
        print("8. View supplier orders")
        print("9. Generate supplier invoice")
        print("10. Process supplier payment")
        print("11. View supplier payment history")
        print("12. Check items needing restock")
        print("13. Schedule automated restock checks")
        choice = input("Enter your choice (1-13): ")
        
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
        elif choice == "6":
            create_supplier_order()
        elif choice == "7":
            update_supplier_order_status()
        elif choice == "8":
            view_supplier_orders()
        elif choice == "9":
            generate_supplier_invoice()
        elif choice == "10":
            process_supplier_payment()
        elif choice == "11":
            view_supplier_payments()
        elif choice == "12":
            check_restock_needed()
        elif choice == "13":
            schedule_restock_check()
    elif response == "14":
        print ("Goodbye!")
        ordering = False
# Supplier performance tracking
supplier_performance = {
    # Format: {supplier_id: {
    #   'total_orders': int,
    #   'on_time_deliveries': int,
    #   'late_deliveries': int,
    #   'quality_issues': int,
    #   'average_delivery_time': float,
    #   'rating': float
    # }}
}

# Delivery status tracking
delivery_history = {
    # Format: {order_id: {
    #   'supplier': str,
    #   'order_date': str,
    #   'delivery_date': str,
    #   'status': 'ontime/late/cancelled',
    #   'quality_score': int
    # }}
}
def record_quality_issue(order_id, issue_description):
    """Record a quality issue with supplier delivery"""
    if order_id not in supplier_orders:
        print("Error: Order not found.")
        return False
    
    order = supplier_orders[order_id]
    supplier_id = order['supplier']
    
    # Initialize performance data if not exists
    if supplier_id not in supplier_performance:
        supplier_performance[supplier_id] = {
            'total_orders': 0,
            'on_time_deliveries': 0,
            'late_deliveries': 0,
            'quality_issues': 0,
            'average_delivery_time': 0,
            'rating': 5.0
        }
    
    # Record quality issue
    supplier_performance[supplier_id]['quality_issues'] += 1
    
    # Update rating based on quality issues
    total_orders = supplier_performance[supplier_id]['total_orders']
    quality_penalty = supplier_performance[supplier_id]['quality_issues'] / total_orders
    supplier_performance[supplier_id]['rating'] = max(0, 5 - (quality_penalty * 2))
    
    # Store quality issue in delivery history
    if order_id not in delivery_history:
        delivery_history[order_id] = {
            'supplier': supplier_id,
            'order_date': order['date'],
            'delivery_date': order['delivery_date'],
            'status': 'delivered',
            'quality_score': 5 - quality_penalty
        }
    
    print(f"Quality issue recorded for supplier {suppliers[supplier_id]['name']}:")
    print(f"Issue: {issue_description}")
    print(f"Updated supplier rating: {supplier_performance[supplier_id]['rating']:.2f}")
    
    return True
def view_supplier_performance():
    """Display supplier performance metrics"""
    print("\n***** Supplier Performance Metrics *****\n")
    
    if not supplier_performance:
        print("No supplier performance data available.")
        return
    
    for supplier_id, metrics in supplier_performance.items():
        supplier_name = suppliers[supplier_id]['name']
        print(f"\nSupplier: {supplier_name}")
        print(f"Total Orders: {metrics['total_orders']}")
        print(f"On-time Deliveries: {metrics['on_time_deliveries']}")
        print(f"Late Deliveries: {metrics['late_deliveries']}")
        
        if metrics['total_orders'] > 0:
            on_time_rate = (metrics['on_time_deliveries'] / metrics['total_orders']) * 100
            print(f"On-time Delivery Rate: {on_time_rate:.1f}%")
        
        print(f"Average Delivery Time: {metrics['average_delivery_time']:.1f} days")
        print(f"Quality Issues: {metrics['quality_issues']}")
        print(f"Current Rating: {metrics['rating']:.2f}/5.0")
        
        # Performance indicators
        if metrics['rating'] >= 4.5:
            print("Performance: Excellent")
        elif metrics['rating'] >= 3.5:
            print("Performance: Good")
        elif metrics['rating'] >= 2.5:
            print("Performance: Average")
        else:
            print("Performance: Poor")
    
    print("\n")
def view_supplier_performance():
    """Display supplier performance metrics"""
    print("\n***** Supplier Performance Metrics *****\n")
    
    if not supplier_performance:
        print("No supplier performance data available.")
        return
    
    for supplier_id, metrics in supplier_performance.items():
        supplier_name = suppliers[supplier_id]['name']
        print(f"\nSupplier: {supplier_name}")
        print(f"Total Orders: {metrics['total_orders']}")
        print(f"On-time Deliveries: {metrics['on_time_deliveries']}")
        print(f"Late Deliveries: {metrics['late_deliveries']}")
        
        if metrics['total_orders'] > 0:
            on_time_rate = (metrics['on_time_deliveries'] / metrics['total_orders']) * 100
            print(f"On-time Delivery Rate: {on_time_rate:.1f}%")
        
        print(f"Average Delivery Time: {metrics['average_delivery_time']:.1f} days")
        print(f"Quality Issues: {metrics['quality_issues']}")
        print(f"Current Rating: {metrics['rating']:.2f}/5.0")
        
        # Performance indicators
        if metrics['rating'] >= 4.5:
            print("Performance: Excellent")
        elif metrics['rating'] >= 3.5:
            print("Performance: Good")
        elif metrics['rating'] >= 2.5:
            print("Performance: Average")
        else:
            print("Performance: Poor")
    
    print("\n")
elif response == "6":
        print("\nWould you like to:")
        print("1. View order history")
        print("2. Request a refund")
        print("3. View inventory")
        print("4. Restock item")
        print("5. Check out-of-stock items")
        print("6. Create supplier order")
        print("7. Update supplier order status")
        print("8. View supplier orders")
        print("9. Generate supplier invoice")
        print("10. Process supplier payment")
        print("11. View supplier payment history")
        print("12. Check items needing restock")
        print("13. Schedule automated restock checks")
        print("14. View supplier performance")
        print("15. Record quality issue")
        choice = input("Enter your choice (1-15): ")
        
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
        elif choice == "6":
            create_supplier_order()
        elif choice == "7":
            update_supplier_order_status()
        elif choice == "8":
            view_supplier_orders()
        elif choice == "9":
            generate_supplier_invoice()
        elif choice == "10":
            process_supplier_payment()
        elif choice == "11":
            view_supplier_payments()
        elif choice == "12":
            check_restock_needed()
        elif choice == "13":
            schedule_restock_check()
        elif choice == "14":
            view_supplier_performance()
        elif choice == "15":
            order_id = input("Enter order ID: ")
            issue_description = input("Describe the quality issue: ")
            record_quality_issue(order_id, issue_description)
    elif response == "16":
        print ("Goodbye!")
        ordering = False
elif response == "6":
        print("\nWould you like to:")
        print("1. View order history")
        print("2. Request a refund")
        print("3. View inventory")
        print("4. Restock item")
        print("5. Check out-of-stock items")
        print("6. Create supplier order")
        print("7. Update supplier order status")
        print("8. View supplier orders")
        print("9. Generate supplier invoice")
        print("10. Process supplier payment")
        print("11. View supplier payment history")
        print("12. Check items needing restock")
        print("13. Schedule automated restock checks")
        print("14. View supplier performance")
        print("15. Record quality issue")
        choice = input("Enter your choice (1-15): ")
        
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
        elif choice == "6":
            create_supplier_order()
        elif choice == "7":
            update_supplier_order_status()
        elif choice == "8":
            view_supplier_orders()
        elif choice == "9":
            generate_supplier_invoice()
        elif choice == "10":
            process_supplier_payment()
        elif choice == "11":
            view_supplier_payments()
        elif choice == "12":
            check_restock_needed()
        elif choice == "13":
            schedule_restock_check()
        elif choice == "14":
            view_supplier_performance()
        elif choice == "15":
            order_id = input("Enter order ID: ")
            issue_description = input("Describe the quality issue: ")
            record_quality_issue(order_id, issue_description)
    elif response == "16":
        print ("Goodbye!")
        ordering = False
elif response == "6":
        print("\nWould you like to:")
        print("1. View order history")
        print("2. Request a refund")
        print("3. View inventory")
        print("4. Restock item")
        print("5. Check out-of-stock items")
        print("6. Create supplier order")
        print("7. Update supplier order status")
        print("8. View supplier orders")
        print("9. Generate supplier invoice")
        print("10. Process supplier payment")
        print("11. View supplier payment history")
        print("12. Check items needing restock")
        print("13. Schedule automated restock checks")
        print("14. View supplier performance")
        print("15. Record quality issue")
        choice = input("Enter your choice (1-15): ")
        
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
        elif choice == "6":
            create_supplier_order()
        elif choice == "7":
            update_supplier_order_status()
        elif choice == "8":
            view_supplier_orders()
        elif choice == "9":
            generate_supplier_invoice()
        elif choice == "10":
            process_supplier_payment()
        elif choice == "11":
            view_supplier_payments()
        elif choice == "12":
            check_restock_needed()
        elif choice == "13":
            schedule_restock_check()
        elif choice == "14":
            view_supplier_performance()
        elif choice == "15":
            order_id = input("Enter order ID: ")
            issue_description = input("Describe the quality issue: ")
            record_quality_issue(order_id, issue_description)
    elif response == "16":
        print ("Goodbye!")
        ordering = False
def update_supplier_order_status():
    """Update the status of a supplier order"""
    print("\n***** Update Supplier Order Status *****\n")
    
    if not supplier_orders:
        print("No supplier orders found.")
        return
    
    print("Pending supplier orders:")
    for order_id, order in supplier_orders.items():
        if order['status'] == 'pending':
            print(f"{order_id} - {suppliers[order['supplier']]['name']} - {order['date']}")
    
    order_id = input("\nEnter order ID to update: ").upper()
    if order_id not in supplier_orders:
        print("Error: Order not found.")
        return
    
    order = supplier_orders[order_id]
    print(f"\nCurrent status: {order['status']}")
    print(f"Items:")
    for sku, quantity in order['items'].items():
        print(f"{inventory[sku]['Name']}: {quantity} units")
    
    if order['status'] == 'pending':
        print("\nSelect new status:")
        print("1. Mark as delivered")
        print("2. Mark as cancelled")
        choice = input("Enter your choice (1-2): ")
        
        if choice == "1":
            # Get delivery date
            delivery_date = input("Enter delivery date (YYYY-MM-DD): ")
            try:
                datetime.strptime(delivery_date, "%Y-%m-%d")
            except ValueError:
                print("Error: Invalid date format.")
                return
            
            # Update order status
            order['status'] = 'delivered'
            order['delivery_date'] = delivery_date
            
            # Update supplier performance
            update_supplier_performance(order_id)
            
            # Update inventory
            for sku, quantity in order['items'].items():
                inventory[sku]['Stock'] += quantity
                print(f"Added {quantity} units of {inventory[sku]['Name']} to inventory.")
            
            print("\nOrder marked as delivered.")
            print("Inventory updated successfully.")
        
        elif choice == "2":
            order['status'] = 'cancelled'
            print("\nOrder has been cancelled.")
        
        else:
            print("Invalid choice.")
    else:
        print("This order cannot be updated.")
def update_supplier_order_status():
    """Update the status of a supplier order"""
    print("\n***** Update Supplier Order Status *****\n")
    
    if not supplier_orders:
        print("No supplier orders found.")
        return
    
    print("Pending supplier orders:")
    for order_id, order in supplier_orders.items():
        if order['status'] == 'pending':
            print(f"{order_id} - {suppliers[order['supplier']]['name']} - {order['date']}")
    
    order_id = input("\nEnter order ID to update: ").upper()
    if order_id not in supplier_orders:
        print("Error: Order not found.")
        return
    
    order = supplier_orders[order_id]
    print(f"\nCurrent status: {order['status']}")
    print(f"Items:")
    for sku, quantity in order['items'].items():
        print(f"{inventory[sku]['Name']}: {quantity} units")
    
    if order['status'] == 'pending':
        print("\nSelect new status:")
        print("1. Mark as delivered")
        print("2. Mark as cancelled")
        choice = input("Enter your choice (1-2): ")
        
        if choice == "1":
            # Get delivery date
            delivery_date = input("Enter delivery date (YYYY-MM-DD): ")
            try:
                datetime.strptime(delivery_date, "%Y-%m-%d")
            except ValueError:
                print("Error: Invalid date format.")
                return
            
            # Update order status
            order['status'] = 'delivered'
            order['delivery_date'] = delivery_date
            
            # Update supplier performance
            update_supplier_performance(order_id)
            
            # Update inventory
            for sku, quantity in order['items'].items():
                inventory[sku]['Stock'] += quantity
                print(f"Added {quantity} units of {inventory[sku]['Name']} to inventory.")
            
            print("\nOrder marked as delivered.")
            print("Inventory updated successfully.")
        
        elif choice == "2":
            order['status'] = 'cancelled'
            print("\nOrder has been cancelled.")
        
        else:
            print("Invalid choice.")
    else:
        print("This order cannot be updated.")
def update_supplier_order_status():
    """Update the status of a supplier order"""
    print("\n***** Update Supplier Order Status *****\n")
    
    if not supplier_orders:
        print("No supplier orders found.")
        return
    
    print("Pending supplier orders:")
    for order_id, order in supplier_orders.items():
        if order['status'] == 'pending':
            print(f"{order_id} - {suppliers[order['supplier']]['name']} - {order['date']}")
    
    order_id = input("\nEnter order ID to update: ").upper()
    if order_id not in supplier_orders:
        print("Error: Order not found.")
        return
    
    order = supplier_orders[order_id]
    print(f"\nCurrent status: {order['status']}")
    print(f"Items:")
    for sku, quantity in order['items'].items():
        print(f"{inventory[sku]['Name']}: {quantity} units")
    
    if order['status'] == 'pending':
        print("\nSelect new status:")
        print("1. Mark as delivered")
        print("2. Mark as cancelled")
        choice = input("Enter your choice (1-2): ")
        
        if choice == "1":
            # Get delivery date
            delivery_date = input("Enter delivery date (YYYY-MM-DD): ")
            try:
                datetime.strptime(delivery_date, "%Y-%m-%d")
            except ValueError:
                print("Error: Invalid date format.")
                return
            
            # Update order status
            order['status'] = 'delivered'
            order['delivery_date'] = delivery_date
            
            # Update supplier performance
            update_supplier_performance(order_id)
            
            # Update inventory
            for sku, quantity in order['items'].items():
                inventory[sku]['Stock'] += quantity
                print(f"Added {quantity} units of {inventory[sku]['Name']} to inventory.")
            
            print("\nOrder marked as delivered.")
            print("Inventory updated successfully.")
        
        elif choice == "2":
            order['status'] = 'cancelled'
            print("\nOrder has been cancelled.")
        
        else:
            print("Invalid choice.")
    else:
        print("This order cannot be updated.")
# Sales tracking for inventory optimization
sales_history = {
    # Format: {date: {sku: {'quantity': int, 'revenue': float}}}
}

# Forecasting parameters
FORECAST_DAYS = 30  # Number of days to forecast
SALES_TREND_DAYS = 7  # Number of days to consider for trend analysis
def record_sale(sku, quantity, price):
    """Record a sale in the sales history"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    if today not in sales_history:
        sales_history[today] = {}
    
    if sku not in sales_history[today]:
        sales_history[today][sku] = {'quantity': 0, 'revenue': 0.0}
    
    sales_history[today][sku]['quantity'] += quantity
    sales_history[today][sku]['revenue'] += price * quantity
    
    return True
def record_sale(sku, quantity, price):
    """Record a sale in the sales history"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    if today not in sales_history:
        sales_history[today] = {}
    
    if sku not in sales_history[today]:
        sales_history[today][sku] = {'quantity': 0, 'revenue': 0.0}
    
    sales_history[today][sku]['quantity'] += quantity
    sales_history[today][sku]['revenue'] += price * quantity
    
    return True
def record_sale(sku, quantity, price):
    """Record a sale in the sales history"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    if today not in sales_history:
        sales_history[today] = {}
    
    if sku not in sales_history[today]:
        sales_history[today][sku] = {'quantity': 0, 'revenue': 0.0}
    
    sales_history[today][sku]['quantity'] += quantity
    sales_history[today][sku]['revenue'] += price * quantity
    
    return True
def record_sale(sku, quantity, price):
    """Record a sale in the sales history"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    if today not in sales_history:
        sales_history[today] = {}
    
    if sku not in sales_history[today]:
        sales_history[today][sku] = {'quantity': 0, 'revenue': 0.0}
    
    sales_history[today][sku]['quantity'] += quantity
    sales_history[today][sku]['revenue'] += price * quantity
    
    return True
def analyze_sales_trends(sku):
    """Analyze sales trends for an item"""
    if sku not in inventory:
        print("Error: Item not found.")
        return None
    
    total_sales = 0
    recent_sales = []
    
    # Get sales data for the trend analysis period
    for date in sorted(sales_history.keys())[-SALES_TREND_DAYS:]:
        if sku in sales_history[date]:
            daily_sales = sales_history[date][sku]['quantity']
            total_sales += daily_sales
            recent_sales.append(daily_sales)
    
    if not recent_sales:
        return {
            'average_daily': 0,
            'trend': 'stable',
            'forecast': 0
        }
    
    # Calculate average daily sales
    average_daily = total_sales / len(recent_sales)
    
    # Determine trend
    if len(recent_sales) >= 3:
        first_half = recent_sales[:len(recent_sales)//2]
        second_half = recent_sales[len(recent_sales)//2:]
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        if second_avg > first_avg * 1.1:
            trend = 'increasing'
        elif second_avg < first_avg * 0.9:
            trend = 'decreasing'
        else:
            trend = 'stable'
    else:
        trend = 'stable'
    
    # Calculate forecast
    if trend == 'increasing':
        forecast = average_daily * 1.2
    elif trend == 'decreasing':
        forecast = average_daily * 0.8
    else:
        forecast = average_daily
    
    return {
        'average_daily': average_daily,
        'trend': trend,
        'forecast': forecast
    }
def analyze_sales_trends(sku):
    """Analyze sales trends for an item"""
    if sku not in inventory:
        print("Error: Item not found.")
        return None
    
    total_sales = 0
    recent_sales = []
    
    # Get sales data for the trend analysis period
    for date in sorted(sales_history.keys())[-SALES_TREND_DAYS:]:
        if sku in sales_history[date]:
            daily_sales = sales_history[date][sku]['quantity']
            total_sales += daily_sales
            recent_sales.append(daily_sales)
    
    if not recent_sales:
        return {
            'average_daily': 0,
            'trend': 'stable',
            'forecast': 0
        }
    
    # Calculate average daily sales
    average_daily = total_sales / len(recent_sales)
    
    # Determine trend
    if len(recent_sales) >= 3:
        first_half = recent_sales[:len(recent_sales)//2]
        second_half = recent_sales[len(recent_sales)//2:]
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        if second_avg > first_avg * 1.1:
            trend = 'increasing'
        elif second_avg < first_avg * 0.9:
            trend = 'decreasing'
        else:
            trend = 'stable'
    else:
        trend = 'stable'
    
    # Calculate forecast
    if trend == 'increasing':
        forecast = average_daily * 1.2
    elif trend == 'decreasing':
        forecast = average_daily * 0.8
    else:
        forecast = average_daily
    
    return {
        'average_daily': average_daily,
        'trend': trend,
        'forecast': forecast
    }
def calculate_optimal_inventory():
    """Calculate optimal inventory levels for all items"""
    print("\n***** Optimal Inventory Levels *****\n")
    
    print("SKU\tItem\tCurrent\tMin\tOptimal\tDays of Stock")
    print("-" * 70)
    
    for sku in inventory:
        item = inventory[sku]
        current_stock = item['Stock']
        min_stock = MINIMUM_STOCK_LEVELS[sku]
        
        # Analyze sales trends
        trend_analysis = analyze_sales_trends(sku)
        if trend_analysis:
            forecast = trend_analysis['forecast']
            optimal_stock = max(min_stock, forecast * FORECAST_DAYS)
            days_of_stock = current_stock / forecast if forecast > 0 else float('inf')
            
            print(f"{sku}\t{item['Name']}\t{current_stock}\t{min_stock}\t{optimal_stock:.0f}\t{days_of_stock:.1f}")
            
            # Provide recommendations
            if current_stock < min_stock:
                print(f"\t⚠️  Action Needed: Current stock below minimum level")
            elif current_stock < optimal_stock:
                print(f"\t⚠️  Action Needed: Consider restocking")
            elif days_of_stock > FORECAST_DAYS * 2:
                print(f"\t⚠️  Action Needed: Excess inventory detected")
            else:
                print(f"\t✓  Stock level optimal")
        else:
            print(f"{sku}\t{item['Name']}\t{current_stock}\t{min_stock}\tN/A\tN/A")
    
    print("\n")
def generate_restock_recommendations():
    """Generate restock recommendations based on sales trends"""
    print("\n***** Restock Recommendations *****\n")
    
    recommendations = []
    
    for sku in inventory:
        item = inventory[sku]
        current_stock = item['Stock']
        
        # Analyze sales trends
        trend_analysis = analyze_sales_trends(sku)
        if trend_analysis:
            forecast = trend_analysis['forecast']
            optimal_stock = max(MINIMUM_STOCK_LEVELS[sku], forecast * FORECAST_DAYS)
            needed = max(0, optimal_stock - current_stock)
            
            if needed > 0:
                priority = "High" if current_stock < MINIMUM_STOCK_LEVELS[sku] else "Medium"
                recommendations.append({
                    'sku': sku,
                    'name': item['Name'],
                    'current': current_stock,
                    'optimal': optimal_stock,
                    'needed': needed,
                    'priority': priority,
                    'trend': trend_analysis['trend']
                })
    
    # Sort recommendations by priority
    recommendations.sort(key=lambda x: (x['priority'] != 'High', x['needed']), reverse=True)
    
    if not recommendations:
        print("No restock recommendations at this time.")
        return
    
    print("Priority\tSKU\tItem\tCurrent\tNeeded\tTrend")
    print("-" * 70)
    
    for rec in recommendations:
        print(f"{rec['priority']}\t{rec['sku']}\t{rec['name']}\t{rec['current']}\t{rec['needed']:.0f}\t{rec['trend']}")
    
    print("\nWould you like to create an order for these recommendations? (yes/no)")
    choice = input().lower()
    
    if choice == 'yes':
        items_to_order = [(rec['sku'], rec['needed']) for rec in recommendations]
        create_automated_order(items_to_order)
    
    print("\n")
def generate_restock_recommendations():
    """Generate restock recommendations based on sales trends"""
    print("\n***** Restock Recommendations *****\n")
    
    recommendations = []
    
    for sku in inventory:
        item = inventory[sku]
        current_stock = item['Stock']
        
        # Analyze sales trends
        trend_analysis = analyze_sales_trends(sku)
        if trend_analysis:
            forecast = trend_analysis['forecast']
            optimal_stock = max(MINIMUM_STOCK_LEVELS[sku], forecast * FORECAST_DAYS)
            needed = max(0, optimal_stock - current_stock)
            
            if needed > 0:
                priority = "High" if current_stock < MINIMUM_STOCK_LEVELS[sku] else "Medium"
                recommendations.append({
                    'sku': sku,
                    'name': item['Name'],
                    'current': current_stock,
                    'optimal': optimal_stock,
                    'needed': needed,
                    'priority': priority,
                    'trend': trend_analysis['trend']
                })
    
    # Sort recommendations by priority
    recommendations.sort(key=lambda x: (x['priority'] != 'High', x['needed']), reverse=True)
    
    if not recommendations:
        print("No restock recommendations at this time.")
        return
    
    print("Priority\tSKU\tItem\tCurrent\tNeeded\tTrend")
    print("-" * 70)
    
    for rec in recommendations:
        print(f"{rec['priority']}\t{rec['sku']}\t{rec['name']}\t{rec['current']}\t{rec['needed']:.0f}\t{rec['trend']}")
    
    print("\nWould you like to create an order for these recommendations? (yes/no)")
    choice = input().lower()
    
    if choice == 'yes':
        items_to_order = [(rec['sku'], rec['needed']) for rec in recommendations]
        create_automated_order(items_to_order)
    
    print("\n")
elif response == "6":
        print("\nWould you like to:")
        print("1. View order history")
        print("2. Request a refund")
        print("3. View inventory")
        print("4. Restock item")
        print("5. Check out-of-stock items")
        print("6. Create supplier order")
        print("7. Update supplier order status")
        print("8. View supplier orders")
        print("9. Generate supplier invoice")
        print("10. Process supplier payment")
        print("11. View supplier payment history")
        print("12. Check items needing restock")
        print("13. Schedule automated restock checks")
        print("14. View supplier performance")
        print("15. Record quality issue")
        print("16. Calculate optimal inventory levels")
        print("17. Generate restock recommendations")
        choice = input("Enter your choice (1-17): ")
        
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
        elif choice == "6":
            create_supplier_order()
        elif choice == "7":
            update_supplier_order_status()
        elif choice == "8":
            view_supplier_orders()
        elif choice == "9":
            generate_supplier_invoice()
        elif choice == "10":
            process_supplier_payment()
        elif choice == "11":
            view_supplier_payments()
        elif choice == "12":
            check_restock_needed()
        elif choice == "13":
            schedule_restock_check()
        elif choice == "14":
            view_supplier_performance()
        elif choice == "15":
            order_id = input("Enter order ID: ")
            issue_description = input("Describe the quality issue: ")
            record_quality_issue(order_id, issue_description)
        elif choice == "16":
            calculate_optimal_inventory()
        elif choice == "17":
            generate_restock_recommendations()
    elif response == "18":
        print ("Goodbye!")
        ordering = False
elif response == "6":
        print("\nWould you like to:")
        print("1. View order history")
        print("2. Request a refund")
        print("3. View inventory")
        print("4. Restock item")
        print("5. Check out-of-stock items")
        print("6. Create supplier order")
        print("7. Update supplier order status")
        print("8. View supplier orders")
        print("9. Generate supplier invoice")
        print("10. Process supplier payment")
        print("11. View supplier payment history")
        print("12. Check items needing restock")
        print("13. Schedule automated restock checks")
        print("14. View supplier performance")
        print("15. Record quality issue")
        print("16. Calculate optimal inventory levels")
        print("17. Generate restock recommendations")
        choice = input("Enter your choice (1-17): ")
        
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
        elif choice == "6":
            create_supplier_order()
        elif choice == "7":
            update_supplier_order_status()
        elif choice == "8":
            view_supplier_orders()
        elif choice == "9":
            generate_supplier_invoice()
        elif choice == "10":
            process_supplier_payment()
        elif choice == "11":
            view_supplier_payments()
        elif choice == "12":
            check_restock_needed()
        elif choice == "13":
            schedule_restock_check()
        elif choice == "14":
            view_supplier_performance()
        elif choice == "15":
            order_id = input("Enter order ID: ")
            issue_description = input("Describe the quality issue: ")
            record_quality_issue(order_id, issue_description)
        elif choice == "16":
            calculate_optimal_inventory()
        elif choice == "17":
            generate_restock_recommendations()
    elif response == "18":
        print ("Goodbye!")
        ordering = False
elif response == "6":
        print("\nWould you like to:")
        print("1. View order history")
        print("2. Request a refund")
        print("3. View inventory")
        print("4. Restock item")
        print("5. Check out-of-stock items")
        print("6. Create supplier order")
        print("7. Update supplier order status")
        print("8. View supplier orders")
        print("9. Generate supplier invoice")
        print("10. Process supplier payment")
        print("11. View supplier payment history")
        print("12. Check items needing restock")
        print("13. Schedule automated restock checks")
        print("14. View supplier performance")
        print("15. Record quality issue")
        print("16. Calculate optimal inventory levels")
        print("17. Generate restock recommendations")
        choice = input("Enter your choice (1-17): ")
        
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
        elif choice == "6":
            create_supplier_order()
        elif choice == "7":
            update_supplier_order_status()
        elif choice == "8":
            view_supplier_orders()
        elif choice == "9":
            generate_supplier_invoice()
        elif choice == "10":
            process_supplier_payment()
        elif choice == "11":
            view_supplier_payments()
        elif choice == "12":
            check_restock_needed()
        elif choice == "13":
            schedule_restock_check()
        elif choice == "14":
            view_supplier_performance()
        elif choice == "15":
            order_id = input("Enter order ID: ")
            issue_description = input("Describe the quality issue: ")
            record_quality_issue(order_id, issue_description)
        elif choice == "16":
            calculate_optimal_inventory()
        elif choice == "17":
            generate_restock_recommendations()
    elif response == "18":
        print ("Goodbye!")
        ordering = False
def checkout():
    # ... existing code ...
    
    if confirm == 'yes':
        # Simulate payment processing
        payment_successful = process_payment(payment_method, total)
        
        if payment_successful:
            # Record sales
            for sku, item in cart.items():
                record_sale(sku, item['quantity'], item['price'])
            
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
            # ... existing code ...
def checkout():
    # ... existing code ...
    
    if confirm == 'yes':
        # Simulate payment processing
        payment_successful = process_payment(payment_method, total)
        
        if payment_successful:
            # Record sales
            for sku, item in cart.items():
                record_sale(sku, item['quantity'], item['price'])
            
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
            # ... existing code ...
# Customer loyalty program
loyalty_members = {
    # Format: {customer_id: {
    #   'name': str,
    #   'points': int,
    #   'tier': str,
    #   'join_date': str,
    #   'total_spent': float,
    #   'visit_count': int
    # }}
}

next_customer_id = 1

# Loyalty program tiers and rewards
LOYALTY_TIERS = {
    'Bronze': {'points_required': 0, 'discount_rate': 0.0, 'rewards': []},
    'Silver': {'points_required': 500, 'discount_rate': 0.05, 'rewards': ['Free dessert']},
    'Gold': {'points_required': 1000, 'discount_rate': 0.1, 'rewards': ['Free dessert', 'Free drink']},
    'Platinum': {'points_required': 2000, 'discount_rate': 0.15, 'rewards': ['Free dessert', 'Free drink', 'Priority seating']}
}

# Points conversion rate
POINTS_PER_DOLLAR = 10
# Customer loyalty program
loyalty_members = {
    # Format: {customer_id: {
    #   'name': str,
    #   'points': int,
    #   'tier': str,
    #   'join_date': str,
    #   'total_spent': float,
    #   'visit_count': int
    # }}
}

next_customer_id = 1

# Loyalty program tiers and rewards
LOYALTY_TIERS = {
    'Bronze': {'points_required': 0, 'discount_rate': 0.0, 'rewards': []},
    'Silver': {'points_required': 500, 'discount_rate': 0.05, 'rewards': ['Free dessert']},
    'Gold': {'points_required': 1000, 'discount_rate': 0.1, 'rewards': ['Free dessert', 'Free drink']},
    'Platinum': {'points_required': 2000, 'discount_rate': 0.15, 'rewards': ['Free dessert', 'Free drink', 'Priority seating']}
}

# Points conversion rate
POINTS_PER_DOLLAR = 10
# Customer loyalty program
loyalty_members = {
    # Format: {customer_id: {
    #   'name': str,
    #   'points': int,
    #   'tier': str,
    #   'join_date': str,
    #   'total_spent': float,
    #   'visit_count': int
    # }}
}

next_customer_id = 1

# Loyalty program tiers and rewards
LOYALTY_TIERS = {
    'Bronze': {'points_required': 0, 'discount_rate': 0.0, 'rewards': []},
    'Silver': {'points_required': 500, 'discount_rate': 0.05, 'rewards': ['Free dessert']},
    'Gold': {'points_required': 1000, 'discount_rate': 0.1, 'rewards': ['Free dessert', 'Free drink']},
    'Platinum': {'points_required': 2000, 'discount_rate': 0.15, 'rewards': ['Free dessert', 'Free drink', 'Priority seating']}
}

# Points conversion rate
POINTS_PER_DOLLAR = 10
# Customer loyalty program
loyalty_members = {
    # Format: {customer_id: {
    #   'name': str,
    #   'points': int,
    #   'tier': str,
    #   'join_date': str,
    #   'total_spent': float,
    #   'visit_count': int
    # }}
}

next_customer_id = 1

# Loyalty program tiers and rewards
LOYALTY_TIERS = {
    'Bronze': {'points_required': 0, 'discount_rate': 0.0, 'rewards': []},
    'Silver': {'points_required': 500, 'discount_rate': 0.05, 'rewards': ['Free dessert']},
    'Gold': {'points_required': 1000, 'discount_rate': 0.1, 'rewards': ['Free dessert', 'Free drink']},
    'Platinum': {'points_required': 2000, 'discount_rate': 0.15, 'rewards': ['Free dessert', 'Free drink', 'Priority seating']}
}

# Points conversion rate
POINTS_PER_DOLLAR = 10
def register_loyalty_member():
    """Register a new customer in the loyalty program"""
    global next_customer_id
    
    print("\n***** Register for Loyalty Program *****\n")
    
    name = input("Enter your full name: ")
    email = input("Enter your email: ")
    phone = input("Enter your phone number: ")
    
    customer_id = f"CUST{next_customer_id:04d}"
    loyalty_members[customer_id] = {
        'name': name,
        'email': email,
        'phone': phone,
        'points': 0,
        'tier': 'Bronze',
        'join_date': datetime.now().strftime("%Y-%m-%d"),
        'total_spent': 0.0,
        'visit_count': 0
    }
    
    next_customer_id += 1
    
    print(f"\nWelcome to the loyalty program, {name}!")
    print(f"Your customer ID is: {customer_id}")
    print("You've automatically been enrolled in the Bronze tier.")
    print("Start earning points with every purchase!")
    
    return customer_id
def update_loyalty_points(customer_id, amount_spent):
    """Update loyalty points based on purchase amount"""
    if customer_id not in loyalty_members:
        print("Error: Customer not found in loyalty program.")
        return False
    
    customer = loyalty_members[customer_id]
    
    # Calculate points earned
    points_earned = int(amount_spent * POINTS_PER_DOLLAR)
    customer['points'] += points_earned
    customer['total_spent'] += amount_spent
    customer['visit_count'] += 1
    
    # Update tier if necessary
    current_tier = customer['tier']
    for tier_name, tier_info in reversed(list(LOYALTY_TIERS.items())):
        if customer['points'] >= tier_info['points_required']:
            if current_tier != tier_name:
                customer['tier'] = tier_name
                print(f"\nCongratulations! You've been upgraded to {tier_name} tier!")
                print(f"New benefits: {', '.join(tier_info['rewards'])}")
            break
    
    print(f"\nPoints earned: {points_earned}")
    print(f"Total points: {customer['points']}")
    print(f"Current tier: {customer['tier']}")
    
    return True
def update_loyalty_points(customer_id, amount_spent):
    """Update loyalty points based on purchase amount"""
    if customer_id not in loyalty_members:
        print("Error: Customer not found in loyalty program.")
        return False
    
    customer = loyalty_members[customer_id]
    
    # Calculate points earned
    points_earned = int(amount_spent * POINTS_PER_DOLLAR)
    customer['points'] += points_earned
    customer['total_spent'] += amount_spent
    customer['visit_count'] += 1
    
    # Update tier if necessary
    current_tier = customer['tier']
    for tier_name, tier_info in reversed(list(LOYALTY_TIERS.items())):
        if customer['points'] >= tier_info['points_required']:
            if current_tier != tier_name:
                customer['tier'] = tier_name
                print(f"\nCongratulations! You've been upgraded to {tier_name} tier!")
                print(f"New benefits: {', '.join(tier_info['rewards'])}")
            break
    
    print(f"\nPoints earned: {points_earned}")
    print(f"Total points: {customer['points']}")
    print(f"Current tier: {customer['tier']}")
    
    return True
def apply_loyalty_discount(customer_id, original_total):
    """Apply loyalty discount to purchase total"""
    if customer_id not in loyalty_members:
        print("Error: Customer not found in loyalty program.")
        return original_total
    
    customer = loyalty_members[customer_id]
    tier_info = LOYALTY_TIERS[customer['tier']]
    
    discount = original_total * tier_info['discount_rate']
    discounted_total = original_total - discount
    
    if discount > 0:
        print(f"\nLoyalty discount applied ({customer['tier']} tier): ${discount:.2f}")
        print(f"New total: ${discounted_total:.2f}")
    
    return discounted_total
def view_loyalty_benefits():
    """Display loyalty program benefits"""
    print("\n***** Loyalty Program Benefits *****\n")
    
    print("Membership Tiers:")
    for tier_name, tier_info in LOYALTY_TIERS.items():
        print(f"\n{tier_name} Tier ({tier_info['points_required']} points required):")
        print(f"  Discount: {tier_info['discount_rate']*100}% off purchases")
        print("  Benefits:")
        for benefit in tier_info['rewards']:
            print(f"  - {benefit}")
    
    print("\nHow to earn points:")
    print(f"  - Earn {POINTS_PER_DOLLAR} points for every $1 spent")
    print("  - Bonus points for special promotions")
    print("  - Points never expire")
    
    print("\nHow to redeem points:")
    print("  - Points automatically applied at checkout")
    print("  - Redeem for discounts on future purchases")
    print("  - Exchange for rewards based on your tier")
    
    print("\n")
def checkout():
    print("\n****Checkout****\n")
    
    # Check if cart is empty
    if not cart:
        print("Your cart is empty. Please add items before checkout.")
        return
    
    # Check if customer is in loyalty program
    print("\nAre you a loyalty member? (yes/no)")
    is_member = input().lower()
    
    customer_id = None
    if is_member == 'yes':
        customer_id = input("Enter your customer ID: ").upper()
        if customer_id not in loyalty_members:
            print("Customer ID not found.")
            print("Would you like to register for the loyalty program? (yes/no)")
            register_choice = input().lower()
            if register_choice == 'yes':
                customer_id = register_loyalty_member()
            else:
                customer_id = None
    elif is_member == 'no':
        print("Would you like to register for the loyalty program? (yes/no)")
        register_choice = input().lower()
        if register_choice == 'yes':
            customer_id = register_loyalty_member()
    
    # Display cart contents
    view_cart()
    
    # Calculate total
    total = calculate_total()
    
    # Apply loyalty discount if applicable
    if customer_id:
        total = apply_loyalty_discount(customer_id, total)
    
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
            
            # Confirm transaction
            print("\nPlease confirm your transaction:")
            confirm = input("Enter 'yes' to confirm or 'no' to cancel: ").lower()
            
            if confirm == 'yes':
                # Simulate payment processing
                payment_successful = process_payment(payment_method, total)
                
                if payment_successful:
                    # Update loyalty points if applicable
                    if customer_id:
                        update_loyalty_points(customer_id, total)
                    
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
elif response == "6":
        print("\nWould you like to:")
        print("1. View order history")
        print("2. Request a refund")
        print("3. View inventory")
        print("4. Restock item")
        print("5. Check out-of-stock items")
        print("6. Create supplier order")
        print("7. Update supplier order status")
        print("8. View supplier orders")
        print("9. Generate supplier invoice")
        print("10. Process supplier payment")
        print("11. View supplier payment history")
        print("12. Check items needing restock")
        print("13. Schedule automated restock checks")
        print("14. View supplier performance")
        print("15. Record quality issue")
        print("16. Calculate optimal inventory levels")
        print("17. Generate restock recommendations")
        print("18. Register for loyalty program")
        print("19. View loyalty benefits")
        choice = input("Enter your choice (1-19): ")
        
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
        elif choice == "6":
            create_supplier_order()
        elif choice == "7":
            update_supplier_order_status()
        elif choice == "8":
            view_supplier_orders()
        elif choice == "9":
            generate_supplier_invoice()
        elif choice == "10":
            process_supplier_payment()
        elif choice == "11":
            view_supplier_payments()
        elif choice == "12":
            check_restock_needed()
        elif choice == "13":
            schedule_restock_check()
        elif choice == "14":
            view_supplier_performance()
        elif choice == "15":
            order_id = input("Enter order ID: ")
            issue_description = input("Describe the quality issue: ")
            record_quality_issue(order_id, issue_description)
        elif choice == "16":
            calculate_optimal_inventory()
        elif choice == "17":
            generate_restock_recommendations()
        elif choice == "18":
            register_loyalty_member()
        elif choice == "19":
            view_loyalty_benefits()
    elif response == "20":
        print ("Goodbye!")
        ordering = False
elif response == "6":
        print("\nWould you like to:")
        print("1. View order history")
        print("2. Request a refund")
        print("3. View inventory")
        print("4. Restock item")
        print("5. Check out-of-stock items")
        print("6. Create supplier order")
        print("7. Update supplier order status")
        print("8. View supplier orders")
        print("9. Generate supplier invoice")
        print("10. Process supplier payment")
        print("11. View supplier payment history")
        print("12. Check items needing restock")
        print("13. Schedule automated restock checks")
        print("14. View supplier performance")
        print("15. Record quality issue")
        print("16. Calculate optimal inventory levels")
        print("17. Generate restock recommendations")
        print("18. Register for loyalty program")
        print("19. View loyalty benefits")
        choice = input("Enter your choice (1-19): ")
        
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
        elif choice == "6":
            create_supplier_order()
        elif choice == "7":
            update_supplier_order_status()
        elif choice == "8":
            view_supplier_orders()
        elif choice == "9":
            generate_supplier_invoice()
        elif choice == "10":
            process_supplier_payment()
        elif choice == "11":
            view_supplier_payments()
        elif choice == "12":
            check_restock_needed()
        elif choice == "13":
            schedule_restock_check()
        elif choice == "14":
            view_supplier_performance()
        elif choice == "15":
            order_id = input("Enter order ID: ")
            issue_description = input("Describe the quality issue: ")
            record_quality_issue(order_id, issue_description)
        elif choice == "16":
            calculate_optimal_inventory()
        elif choice == "17":
            generate_restock_recommendations()
        elif choice == "18":
            register_loyalty_member()
        elif choice == "19":
            view_loyalty_benefits()
    elif response == "20":
        print ("Goodbye!")
        ordering = False
# Gift card system
gift_cards = {
    # Format: {card_number: {
    #   'balance': float,
    #   'is_active': bool,
    #   'issue_date': str,
    #   'expiry_date': str,
    #   'customer_id': str (optional)
    # }}
}

next_card_number = 1

# Gift card settings
GIFT_CARD_EXPIRY_DAYS = 365  # 1 year
MIN_GIFT_CARD_AMOUNT = 10
MAX_GIFT_CARD_AMOUNT = 500
# Gift card system
gift_cards = {
    # Format: {card_number: {
    #   'balance': float,
    #   'is_active': bool,
    #   'issue_date': str,
    #   'expiry_date': str,
    #   'customer_id': str (optional)
    # }}
}

next_card_number = 1

# Gift card settings
GIFT_CARD_EXPIRY_DAYS = 365  # 1 year
MIN_GIFT_CARD_AMOUNT = 10
MAX_GIFT_CARD_AMOUNT = 500
def issue_gift_card():
    """Issue a new gift card"""
    global next_card_number
    
    print("\n***** Issue Gift Card *****\n")
    
    try:
        amount = float(input("Enter gift card amount: $"))
        if amount < MIN_GIFT_CARD_AMOUNT or amount > MAX_GIFT_CARD_AMOUNT:
            print(f"Gift card amount must be between ${MIN_GIFT_CARD_AMOUNT} and ${MAX_GIFT_CARD_AMOUNT}")
            return None
    except ValueError:
        print("Invalid amount entered.")
        return None
    
    # Generate unique card number
    card_number = f"GIFT{next_card_number:08d}"
    next_card_number += 1
    
    # Calculate expiry date
    issue_date = datetime.now()
    expiry_date = issue_date + timedelta(days=GIFT_CARD_EXPIRY_DAYS)
    
    # Create gift card
    gift_cards[card_number] = {
        'balance': amount,
        'is_active': True,
        'issue_date': issue_date.strftime("%Y-%m-%d"),
        'expiry_date': expiry_date.strftime("%Y-%m-%d"),
        'customer_id': None
    }
    
    print(f"\nGift card issued successfully!")
    print(f"Card Number: {card_number}")
    print(f"Amount: ${amount:.2f}")
    print(f"Expiry Date: {expiry_date.strftime('%Y-%m-%d')}")
    print("\nPlease keep this card number safe for future use.")
    
    return card_number
def issue_gift_card():
    """Issue a new gift card"""
    global next_card_number
    
    print("\n***** Issue Gift Card *****\n")
    
    try:
        amount = float(input("Enter gift card amount: $"))
        if amount < MIN_GIFT_CARD_AMOUNT or amount > MAX_GIFT_CARD_AMOUNT:
            print(f"Gift card amount must be between ${MIN_GIFT_CARD_AMOUNT} and ${MAX_GIFT_CARD_AMOUNT}")
            return None
    except ValueError:
        print("Invalid amount entered.")
        return None
    
    # Generate unique card number
    card_number = f"GIFT{next_card_number:08d}"
    next_card_number += 1
    
    # Calculate expiry date
    issue_date = datetime.now()
    expiry_date = issue_date + timedelta(days=GIFT_CARD_EXPIRY_DAYS)
    
    # Create gift card
    gift_cards[card_number] = {
        'balance': amount,
        'is_active': True,
        'issue_date': issue_date.strftime("%Y-%m-%d"),
        'expiry_date': expiry_date.strftime("%Y-%m-%d"),
        'customer_id': None
    }
    
    print(f"\nGift card issued successfully!")
    print(f"Card Number: {card_number}")
    print(f"Amount: ${amount:.2f}")
    print(f"Expiry Date: {expiry_date.strftime('%Y-%m-%d')}")
    print("\nPlease keep this card number safe for future use.")
    
    return card_number
def check_gift_card_balance(card_number):
    """Check the balance of a gift card"""
    if card_number not in gift_cards:
        print("Error: Invalid card number.")
        return None
    
    card = gift_cards[card_number]
    
    if not card['is_active']:
        print("Error: This gift card has been deactivated.")
        return None
    
    # Check if card is expired
    expiry_date = datetime.strptime(card['expiry_date'], "%Y-%m-%d")
    if datetime.now() > expiry_date:
        print("Error: This gift card has expired.")
        return None
    
    print(f"\nGift Card Details:")
    print(f"Card Number: {card_number}")
    print(f"Balance: ${card['balance']:.2f}")
    print(f"Expiry Date: {card['expiry_date']}")
    
    return card['balance']
def check_gift_card_balance(card_number):
    """Check the balance of a gift card"""
    if card_number not in gift_cards:
        print("Error: Invalid card number.")
        return None
    
    card = gift_cards[card_number]
    
    if not card['is_active']:
        print("Error: This gift card has been deactivated.")
        return None
    
    # Check if card is expired
    expiry_date = datetime.strptime(card['expiry_date'], "%Y-%m-%d")
    if datetime.now() > expiry_date:
        print("Error: This gift card has expired.")
        return None
    
    print(f"\nGift Card Details:")
    print(f"Card Number: {card_number}")
    print(f"Balance: ${card['balance']:.2f}")
    print(f"Expiry Date: {card['expiry_date']}")
    
    return card['balance']
def apply_gift_card(card_number, amount):
    """Apply gift card balance to purchase"""
    if card_number not in gift_cards:
        print("Error: Invalid card number.")
        return 0
    
    card = gift_cards[card_number]
    
    if not card['is_active']:
        print("Error: This gift card has been deactivated.")
        return 0
    
    # Check if card is expired
    expiry_date = datetime.strptime(card['expiry_date'], "%Y-%m-%d")
    if datetime.now() > expiry_date:
        print("Error: This gift card has expired.")
        return 0
    
    # Calculate amount to apply
    apply_amount = min(amount, card['balance'])
    card['balance'] -= apply_amount
    
    if card['balance'] == 0:
        card['is_active'] = False
        print("Gift card balance fully used.")
    else:
        print(f"Remaining gift card balance: ${card['balance']:.2f}")
    
    return apply_amount
def apply_gift_card(card_number, amount):
    """Apply gift card balance to purchase"""
    if card_number not in gift_cards:
        print("Error: Invalid card number.")
        return 0
    
    card = gift_cards[card_number]
    
    if not card['is_active']:
        print("Error: This gift card has been deactivated.")
        return 0
    
    # Check if card is expired
    expiry_date = datetime.strptime(card['expiry_date'], "%Y-%m-%d")
    if datetime.now() > expiry_date:
        print("Error: This gift card has expired.")
        return 0
    
    # Calculate amount to apply
    apply_amount = min(amount, card['balance'])
    card['balance'] -= apply_amount
    
    if card['balance'] == 0:
        card['is_active'] = False
        print("Gift card balance fully used.")
    else:
        print(f"Remaining gift card balance: ${card['balance']:.2f}")
    
    return apply_amount
# Payment processing
            print("\nPlease select your payment method:")
            print("1. Credit Card")
            print("2. Cash")
            print("3. Gift Card")
            payment_method = input("Enter your choice (1-3): ")
            
            max_retries = 3
            retry_count = 0
            gift_card_amount = 0
            
            if payment_method == "3":
                # Gift card payment
                card_number = input("Enter gift card number: ").upper()
                gift_card_balance = check_gift_card_balance(card_number)
                if gift_card_balance is None:
                    print("Invalid gift card. Please try again.")
                    continue
                
                if gift_card_balance >= total:
                    gift_card_amount = total
                    remaining_amount = 0
                else:
                    gift_card_amount = gift_card_balance
                    remaining_amount = total - gift_card_balance
                    print(f"Gift card balance: ${gift_card_balance:.2f}")
                    print(f"Remaining amount: ${remaining_amount:.2f}")
                    print("Please select additional payment method for remaining amount:")
                    print("1. Credit Card")
                    print("2. Cash")
                    additional_payment = input("Enter your choice (1-2): ")
                    
                    if additional_payment == "1":
                        card_number = input("Enter credit card number: ")
                        if len(card_number) != 16 or not card_number.isdigit():
                            print("Invalid credit card number.")
                            continue
                        expiry_date = input("Enter expiry date (MM/YY): ")
                        cvv = input("Enter CVV: ")
                        if len(cvv) != 3 or not cvv.isdigit():
                            print("Invalid CVV.")
                            continue
                    elif additional_payment == "2":
                        pass
                    else:
                        print("Invalid payment method.")
                        continue
            
            max_retries = 3
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    if payment_method == "1":
                        # Credit card processing
                        if payment_method not in ["1", "2", "3"]:
                            raise ValueError("Invalid payment method selected.")
                        
                        if payment_method == "1":
                            card_number = input("Enter your credit card number: ")
                            if len(card_number) != 16 or not card_number.isdigit():
                                raise ValueError("Invalid credit card number.")
                            expiry_date = input("Enter expiry date (MM/YY): ")
                            cvv = input("Enter CVV: ")
                            if len(cvv) != 3 or not cvv.isdigit():
                                raise ValueError("Invalid CVV.")
                    
                    # Confirm transaction
                    print("\nPlease confirm your transaction:")
                    print(f"Total amount: ${total:.2f}")
                    if gift_card_amount > 0:
                        print(f"Gift card payment: ${gift_card_amount:.2f}")
                        if remaining_amount > 0:
                            print(f"Additional payment: ${remaining_amount:.2f}")
                    confirm = input("Enter 'yes' to confirm or 'no' to cancel: ").lower()
                    
                    if confirm == 'yes':
                        # Process payment
                        payment_successful = True
                        
                        if payment_method == "3":
                            # Apply gift card
                            if gift_card_amount > 0:
                                apply_gift_card(card_number, gift_card_amount)
                                if remaining_amount > 0:
                                    if additional_payment == "1":
                                        payment_successful = process_payment(additional_payment, remaining_amount)
                                    else:
                                        # Cash payment - assume successful
                                        pass
                        
                        if payment_successful:
                            # Update loyalty points if applicable
                            if customer_id:
                                update_loyalty_points(customer_id, total)
                            
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
                                continue
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
# Payment processing
            print("\nPlease select your payment method:")
            print("1. Credit Card")
            print("2. Cash")
            print("3. Gift Card")
            payment_method = input("Enter your choice (1-3): ")
            
            max_retries = 3
            retry_count = 0
            gift_card_amount = 0
            
            if payment_method == "3":
                # Gift card payment
                card_number = input("Enter gift card number: ").upper()
                gift_card_balance = check_gift_card_balance(card_number)
                if gift_card_balance is None:
                    print("Invalid gift card. Please try again.")
                    continue
                
                if gift_card_balance >= total:
                    gift_card_amount = total
                    remaining_amount = 0
                else:
                    gift_card_amount = gift_card_balance
                    remaining_amount = total - gift_card_balance
                    print(f"Gift card balance: ${gift_card_balance:.2f}")
                    print(f"Remaining amount: ${remaining_amount:.2f}")
                    print("Please select additional payment method for remaining amount:")
                    print("1. Credit Card")
                    print("2. Cash")
                    additional_payment = input("Enter your choice (1-2): ")
                    
                    if additional_payment == "1":
                        card_number = input("Enter credit card number: ")
                        if len(card_number) != 16 or not card_number.isdigit():
                            print("Invalid credit card number.")
                            continue
                        expiry_date = input("Enter expiry date (MM/YY): ")
                        cvv = input("Enter CVV: ")
                        if len(cvv) != 3 or not cvv.isdigit():
                            print("Invalid CVV.")
                            continue
                    elif additional_payment == "2":
                        pass
                    else:
                        print("Invalid payment method.")
                        continue
            
            max_retries = 3
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    if payment_method == "1":
                        # Credit card processing
                        if payment_method not in ["1", "2", "3"]:
                            raise ValueError("Invalid payment method selected.")
                        
                        if payment_method == "1":
                            card_number = input("Enter your credit card number: ")
                            if len(card_number) != 16 or not card_number.isdigit():
                                raise ValueError("Invalid credit card number.")
                            expiry_date = input("Enter expiry date (MM/YY): ")
                            cvv = input("Enter CVV: ")
                            if len(cvv) != 3 or not cvv.isdigit():
                                raise ValueError("Invalid CVV.")
                    
                    # Confirm transaction
                    print("\nPlease confirm your transaction:")
                    print(f"Total amount: ${total:.2f}")
                    if gift_card_amount > 0:
                        print(f"Gift card payment: ${gift_card_amount:.2f}")
                        if remaining_amount > 0:
                            print(f"Additional payment: ${remaining_amount:.2f}")
                    confirm = input("Enter 'yes' to confirm or 'no' to cancel: ").lower()
                    
                    if confirm == 'yes':
                        # Process payment
                        payment_successful = True
                        
                        if payment_method == "3":
                            # Apply gift card
                            if gift_card_amount > 0:
                                apply_gift_card(card_number, gift_card_amount)
                                if remaining_amount > 0:
                                    if additional_payment == "1":
                                        payment_successful = process_payment(additional_payment, remaining_amount)
                                    else:
                                        # Cash payment - assume successful
                                        pass
                        
                        if payment_successful:
                            # Update loyalty points if applicable
                            if customer_id:
                                update_loyalty_points(customer_id, total)
                            
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
                                continue
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
elif response == "6":
        print("\nWould you like to:")
        print("1. View order history")
        print("2. Request a refund")
        print("3. View inventory")
        print("4. Restock item")
        print("5. Check out-of-stock items")
        print("6. Create supplier order")
        print("7. Update supplier order status")
        print("8. View supplier orders")
        print("9. Generate supplier invoice")
        print("10. Process supplier payment")
        print("11. View supplier payment history")
        print("12. Check items needing restock")
        print("13. Schedule automated restock checks")
        print("14. View supplier performance")
        print("15. Record quality issue")
        print("16. Calculate optimal inventory levels")
        print("17. Generate restock recommendations")
        print("18. Register for loyalty program")
        print("19. View loyalty benefits")
        print("20. Issue gift card")
        print("21. Check gift card balance")
        choice = input("Enter your choice (1-21): ")
        
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
        elif choice == "6":
            create_supplier_order()
        elif choice == "7":
            update_supplier_order_status()
        elif choice == "8":
            view_supplier_orders()
        elif choice == "9":
            generate_supplier_invoice()
        elif choice == "10":
            process_supplier_payment()
        elif choice == "11":
            view_supplier_payments()
        elif choice == "12":
            check_restock_needed()
        elif choice == "13":
            schedule_restock_check()
        elif choice == "14":
            view_supplier_performance()
        elif choice == "15":
            order_id = input("Enter order ID: ")
            issue_description = input("Describe the quality issue: ")
            record_quality_issue(order_id, issue_description)
        elif choice == "16":
            calculate_optimal_inventory()
        elif choice == "17":
            generate_restock_recommendations()
        elif choice == "18":
            register_loyalty_member()
        elif choice == "19":
            view_loyalty_benefits()
        elif choice == "20":
            issue_gift_card()
        elif choice == "21":
            card_number = input("Enter gift card number: ").upper()
            check_gift_card_balance(card_number)
    elif response == "22":
        print ("Goodbye!")
        ordering = False
elif response == "6":
        print("\nWould you like to:")
        print("1. View order history")
        print("2. Request a refund")
        print("3. View inventory")
        print("4. Restock item")
        print("5. Check out-of-stock items")
        print("6. Create supplier order")
        print("7. Update supplier order status")
        print("8. View supplier orders")
        print("9. Generate supplier invoice")
        print("10. Process supplier payment")
        print("11. View supplier payment history")
        print("12. Check items needing restock")
        print("13. Schedule automated restock checks")
        print("14. View supplier performance")
        print("15. Record quality issue")
        print("16. Calculate optimal inventory levels")
        print("17. Generate restock recommendations")
        print("18. Register for loyalty program")
        print("19. View loyalty benefits")
        print("20. Issue gift card")
        print("21. Check gift card balance")
        choice = input("Enter your choice (1-21): ")
        
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
        elif choice == "6":
            create_supplier_order()
        elif choice == "7":
            update_supplier_order_status()
        elif choice == "8":
            view_supplier_orders()
        elif choice == "9":
            generate_supplier_invoice()
        elif choice == "10":
            process_supplier_payment()
        elif choice == "11":
            view_supplier_payments()
        elif choice == "12":
            check_restock_needed()
        elif choice == "13":
            schedule_restock_check()
        elif choice == "14":
            view_supplier_performance()
        elif choice == "15":
            order_id = input("Enter order ID: ")
            issue_description = input("Describe the quality issue: ")
            record_quality_issue(order_id, issue_description)
        elif choice == "16":
            calculate_optimal_inventory()
        elif choice == "17":
            generate_restock_recommendations()
        elif choice == "18":
            register_loyalty_member()
        elif choice == "19":
            view_loyalty_benefits()
        elif choice == "20":
            issue_gift_card()
        elif choice == "21":
            card_number = input("Enter gift card number: ").upper()
            check_gift_card_balance(card_number)
    elif response == "22":
        print ("Goodbye!")
        ordering = False
elif response == "6":
        print("\nWould you like to:")
        print("1. View order history")
        print("2. Request a refund")
        print("3. View inventory")
        print("4. Restock item")
        print("5. Check out-of-stock items")
        print("6. Create supplier order")
        print("7. Update supplier order status")
        print("8. View supplier orders")
        print("9. Generate supplier invoice")
        print("10. Process supplier payment")
        print("11. View supplier payment history")
        print("12. Check items needing restock")
        print("13. Schedule automated restock checks")
        print("14. View supplier performance")
        print("15. Record quality issue")
        print("16. Calculate optimal inventory levels")
        print("17. Generate restock recommendations")
        print("18. Register for loyalty program")
        print("19. View loyalty benefits")
        print("20. Issue gift card")
        print("21. Check gift card balance")
        choice = input("Enter your choice (1-21): ")
        
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
        elif choice == "6":
            create_supplier_order()
        elif choice == "7":
            update_supplier_order_status()
        elif choice == "8":
            view_supplier_orders()
        elif choice == "9":
            generate_supplier_invoice()
        elif choice == "10":
            process_supplier_payment()
        elif choice == "11":
            view_supplier_payments()
        elif choice == "12":
            check_restock_needed()
        elif choice == "13":
            schedule_restock_check()
        elif choice == "14":
            view_supplier_performance()
        elif choice == "15":
            order_id = input("Enter order ID: ")
            issue_description = input("Describe the quality issue: ")
            record_quality_issue(order_id, issue_description)
        elif choice == "16":
            calculate_optimal_inventory()
        elif choice == "17":
            generate_restock_recommendations()
        elif choice == "18":
            register_loyalty_member()
        elif choice == "19":
            view_loyalty_benefits()
        elif choice == "20":
            issue_gift_card()
        elif choice == "21":
            card_number = input("Enter gift card number: ").upper()
            check_gift_card_balance(card_number)
    elif response == "22":
        print ("Goodbye!")
        ordering = False
   item = MENU[sku]['Name']
        price = MENU[sku]['Price']
        stock = inventory[sku]['Stock']
        if stock == 0:
            print("("+ sku + ")" + " " + item + ": $" + str(price) + " - OUT OF STOCK")
        else:
            print("("+ sku + ")" + " " + item + ": $" + str(price) + " (Stock: " + str<codegeex-cursor></codegeex-cursor>
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
def create_supplier_order():
    """Create a new supplier order"""
    global next_supplier_order_id
    
    print("\n***** Create Supplier Order *****\n")
    print("Available suppliers:")
    for supplier_id, supplier in suppliers.items():
        print(f"({supplier_id}) {supplier['name']} (Lead time: {supplier['lead_time']} days)")
    
    supplier_id = input("\nEnter supplier ID: ").upper()
    if supplier_id not in suppliers:
        print("Error: Invalid supplier ID.")
        return False
    
    order_id = f"SO{next_supplier_order_id:04d}"
    supplier_orders[order_id] = {
        'supplier': supplier_id,
        'items': {},
        'status': 'pending',
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'expected_delivery': (datetime.now() + timedelta(days=suppliers[supplier_id]['lead_time'])).strftime("%Y-%m-%d")
    }
    
    print(f"\nNew supplier order created: {order_id}")
    print(f"Supplier: {suppliers[supplier_id]['name']}")
    print(f"Expected delivery: {supplier_orders[order_id]['expected_delivery']}")
    
    while True:
        print("\nAdd items to order:")
        print("1. Add item")
        print("2. Finish order")
        choice = input("Enter your choice (1-2): ")
        
        if choice == "1":
            print("\nAvailable items:")
            for sku, item in inventory.items():
                print(f"({sku}) {item['Name']} - Current stock: {item['Stock']}")
            
            sku = input("\nEnter item SKU: ")
            if sku not in inventory:
                print("Error: Invalid item SKU.")
                continue
            
            try:
                quantity = int(input("Enter quantity to order: "))
                if quantity <= 0:
                    print("Error: Quantity must be positive.")
                    continue
            except ValueError:
                print("Error: Invalid quantity.")
                continue
            
            if sku in supplier_orders[order_id]['items']:
                supplier_orders[order_id]['items'][sku] += quantity
            else:
                supplier_orders[order_id]['items'][sku] = quantity
            
            print(f"Added {quantity} units of {inventory[sku]['Name']} to order.")
        
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")
    
    # Calculate order total
    total = 0
    for sku, quantity in supplier_orders[order_id]['items'].items():
        total += inventory[sku]['Price'] * quantity
    
    supplier_orders[order_id]['total'] = total
    print(f"\nOrder total: ${total:.2f}")
    print(f"Order {order_id} created successfully.")
    
    next_supplier_order_id += 1
    return order_id
def create_supplier_order():
    """Create a new supplier order"""
    global next_supplier_order_id
    
    print("\n***** Create Supplier Order *****\n")
    print("Available suppliers:")
    for supplier_id, supplier in suppliers.items():
        print(f"({supplier_id}) {supplier['name']} (Lead time: {supplier['lead_time']} days)")
    
    supplier_id = input("\nEnter supplier ID: ").upper()
    if supplier_id not in suppliers:
        print("Error: Invalid supplier ID.")
        return False
    
    order_id = f"SO{next_supplier_order_id:04d}"
    supplier_orders[order_id] = {
        'supplier': supplier_id,
        'items': {},
        'status': 'pending',
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'expected_delivery': (datetime.now() + timedelta(days=suppliers[supplier_id]['lead_time'])).strftime("%Y-%m-%d")
    }
    
    print(f"\nNew supplier order created: {order_id}")
    print(f"Supplier: {suppliers[supplier_id]['name']}")
    print(f"Expected delivery: {supplier_orders[order_id]['expected_delivery']}")
    
    while True:
        print("\nAdd items to order:")
        print("1. Add item")
        print("2. Finish order")
        choice = input("Enter your choice (1-2): ")
        
        if choice == "1":
            print("\nAvailable items:")
            for sku, item in inventory.items():
                print(f"({sku}) {item['Name']} - Current stock: {item['Stock']}")
            
            sku = input("\nEnter item SKU: ")
            if sku not in inventory:
                print("Error: Invalid item SKU.")
                continue
            
            try:
                quantity = int(input("Enter quantity to order: "))
                if quantity <= 0:
                    print("Error: Quantity must be positive.")
                    continue
            except ValueError:
                print("Error: Invalid quantity.")
                continue
            
            if sku in supplier_orders[order_id]['items']:
                supplier_orders[order_id]['items'][sku] += quantity
            else:
                supplier_orders[order_id]['items'][sku] = quantity
            
            print(f"Added {quantity} units of {inventory[sku]['Name']} to order.")
        
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")
    
    # Calculate order total
    total = 0
    for sku, quantity in supplier_orders[order_id]['items'].items():
        total += inventory[sku]['Price'] * quantity
    
    supplier_orders[order_id]['total'] = total
    print(f"\nOrder total: ${total:.2f}")
    print(f"Order {order_id} created successfully.")
    
    next_supplier_order_id += 1
    return order_id
def create_supplier_order():
    """Create a new supplier order"""
    global next_supplier_order_id
    
    print("\n***** Create Supplier Order *****\n")
    print("Available suppliers:")
    for supplier_id, supplier in suppliers.items():
        print(f"({supplier_id}) {supplier['name']} (Lead time: {supplier['lead_time']} days)")
    
    supplier_id = input("\nEnter supplier ID: ").upper()
    if supplier_id not in suppliers:
        print("Error: Invalid supplier ID.")
        return False
    
    order_id = f"SO{next_supplier_order_id:04d}"
    supplier_orders[order_id] = {
        'supplier': supplier_id,
        'items': {},
        'status': 'pending',
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'expected_delivery': (datetime.now() + timedelta(days=suppliers[supplier_id]['lead_time'])).strftime("%Y-%m-%d")
    }
    
    print(f"\nNew supplier order created: {order_id}")
    print(f"Supplier: {suppliers[supplier_id]['name']}")
    print(f"Expected delivery: {supplier_orders[order_id]['expected_delivery']}")
    
    while True:
        print("\nAdd items to order:")
        print("1. Add item")
        print("2. Finish order")
        choice = input("Enter your choice (1-2): ")
        
        if choice == "1":
            print("\nAvailable items:")
            for sku, item in inventory.items():
                print(f"({sku}) {item['Name']} - Current stock: {item['Stock']}")
            
            sku = input("\nEnter item SKU: ")
            if sku not in inventory:
                print("Error: Invalid item SKU.")
                continue
            
            try:
                quantity = int(input("Enter quantity to order: "))
                if quantity <= 0:
                    print("Error: Quantity must be positive.")
                    continue
            except ValueError:
                print("Error: Invalid quantity.")
                continue
            
            if sku in supplier_orders[order_id]['items']:
                supplier_orders[order_id]['items'][sku] += quantity
            else:
                supplier_orders[order_id]['items'][sku] = quantity
            
            print(f"Added {quantity} units of {inventory[sku]['Name']} to order.")
        
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")
    
    # Calculate order total
    total = 0
    for sku, quantity in supplier_orders[order_id]['items'].items():
        total += inventory[sku]['Price'] * quantity
    
    supplier_orders[order_id]['total'] = total
    print(f"\nOrder total: ${total:.2f}")
    print(f"Order {order_id} created successfully.")
    
    next_supplier_order_id += 1
    return order_id
def create_supplier_order():
    """Create a new supplier order"""
    global next_supplier_order_id
    
    print("\n***** Create Supplier Order *****\n")
    print("Available suppliers:")
    for supplier_id, supplier in suppliers.items():
        print(f"({supplier_id}) {supplier['name']} (Lead time: {supplier['lead_time']} days)")
    
    supplier_id = input("\nEnter supplier ID: ").upper()
    if supplier_id not in suppliers:
        print("Error: Invalid supplier ID.")
        return False
    
    order_id = f"SO{next_supplier_order_id:04d}"
    supplier_orders[order_id] = {
        'supplier': supplier_id,
        'items': {},
        'status': 'pending',
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'expected_delivery': (datetime.now() + timedelta(days=suppliers[supplier_id]['lead_time'])).strftime("%Y-%m-%d")
    }
    
    print(f"\nNew supplier order created: {order_id}")
    print(f"Supplier: {suppliers[supplier_id]['name']}")
    print(f"Expected delivery: {supplier_orders[order_id]['expected_delivery']}")
    
    while True:
        print("\nAdd items to order:")
        print("1. Add item")
        print("2. Finish order")
        choice = input("Enter your choice (1-2): ")
        
        if choice == "1":
            print("\nAvailable items:")
            for sku, item in inventory.items():
                print(f"({sku}) {item['Name']} - Current stock: {item['Stock']}")
            
            sku = input("\nEnter item SKU: ")
            if sku not in inventory:
                print("Error: Invalid item SKU.")
                continue
            
            try:
                quantity = int(input("Enter quantity to order: "))
                if quantity <= 0:
                    print("Error: Quantity must be positive.")
                    continue
            except ValueError:
                print("Error: Invalid quantity.")
                continue
            
            if sku in supplier_orders[order_id]['items']:
                supplier_orders[order_id]['items'][sku] += quantity
            else:
                supplier_orders[order_id]['items'][sku] = quantity
            
            print(f"Added {quantity} units of {inventory[sku]['Name']} to order.")
        
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")
    
    # Calculate order total
    total = 0
    for sku, quantity in supplier_orders[order_id]['items'].items():
        total += inventory[sku]['Price'] * quantity
    
    supplier_orders[order_id]['total'] = total
    print(f"\nOrder total: ${total:.2f}")
    print(f"Order {order_id} created successfully.")
    
    next_supplier_order_id += 1
    return order_id
def create_supplier_order():
    """Create a new supplier order"""
    global next_supplier_order_id
    
    print("\n***** Create Supplier Order *****\n")
    print("Available suppliers:")
    for supplier_id, supplier in suppliers.items():
        print(f"({supplier_id}) {supplier['name']} (Lead time: {supplier['lead_time']} days)")
    
    supplier_id = input("\nEnter supplier ID: ").upper()
    if supplier_id not in suppliers:
        print("Error: Invalid supplier ID.")
        return False
    
    order_id = f"SO{next_supplier_order_id:04d}"
    supplier_orders[order_id] = {
        'supplier': supplier_id,
        'items': {},
        'status': 'pending',
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'expected_delivery': (datetime.now() + timedelta(days=suppliers[supplier_id]['lead_time'])).strftime("%Y-%m-%d")
    }
    
    print(f"\nNew supplier order created: {order_id}")
    print(f"Supplier: {suppliers[supplier_id]['name']}")
    print(f"Expected delivery: {supplier_orders[order_id]['expected_delivery']}")
    
    while True:
        print("\nAdd items to order:")
        print("1. Add item")
        print("2. Finish order")
        choice = input("Enter your choice (1-2): ")
        
        if choice == "1":
            print("\nAvailable items:")
            for sku, item in inventory.items():
                print(f"({sku}) {item['Name']} - Current stock: {item['Stock']}")
            
            sku = input("\nEnter item SKU: ")
            if sku not in inventory:
                print("Error: Invalid item SKU.")
                continue
            
            try:
                quantity = int(input("Enter quantity to order: "))
                if quantity <= 0:
                    print("Error: Quantity must be positive.")
                    continue
            except ValueError:
                print("Error: Invalid quantity.")
                continue
            
            if sku in supplier_orders[order_id]['items']:
                supplier_orders[order_id]['items'][sku] += quantity
            else:
                supplier_orders[order_id]['items'][sku] = quantity
            
            print(f"Added {quantity} units of {inventory[sku]['Name']} to order.")
        
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")
    
    # Calculate order total
    total = 0
    for sku, quantity in supplier_orders[order_id]['items'].items():
        total += inventory[sku]['Price'] * quantity
    
    supplier_orders[order_id]['total'] = total
    print(f"\nOrder total: ${total:.2f}")
    print(f"Order {order_id} created successfully.")
    
    next_supplier_order_id += 1
    return order_id
def create_supplier_order():
    """Create a new supplier order"""
    global next_supplier_order_id
    
    print("\n***** Create Supplier Order *****\n")
    print("Available suppliers:")
    for supplier_id, supplier in suppliers.items():
        print(f"({supplier_id}) {supplier['name']} (Lead time: {supplier['lead_time']} days)")
    
    supplier_id = input("\nEnter supplier ID: ").upper()
    if supplier_id not in suppliers:
        print("Error: Invalid supplier ID.")
        return False
    
    order_id = f"SO{next_supplier_order_id:04d}"
    supplier_orders[order_id] = {
        'supplier': supplier_id,
        'items': {},
        'status': 'pending',
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'expected_delivery': (datetime.now() + timedelta(days=suppliers[supplier_id]['lead_time'])).strftime("%Y-%m-%d")
    }
    
    print(f"\nNew supplier order created: {order_id}")
    print(f"Supplier: {suppliers[supplier_id]['name']}")
    print(f"Expected delivery: {supplier_orders[order_id]['expected_delivery']}")
    
    while True:
        print("\nAdd items to order:")
        print("1. Add item")
        print("2. Finish order")
        choice = input("Enter your choice (1-2): ")
        
        if choice == "1":
            print("\nAvailable items:")
            for sku, item in inventory.items():
                print(f"({sku}) {item['Name']} - Current stock: {item['Stock']}")
            
            sku = input("\nEnter item SKU: ")
            if sku not in inventory:
                print("Error: Invalid item SKU.")
                continue
            
            try:
                quantity = int(input("Enter quantity to order: "))
                if quantity <= 0:
                    print("Error: Quantity must be positive.")
                    continue
            except ValueError:
                print("Error: Invalid quantity.")
                continue
            
            if sku in supplier_orders[order_id]['items']:
                supplier_orders[order_id]['items'][sku] += quantity
            else:
                supplier_orders[order_id]['items'][sku] = quantity
            
            print(f"Added {quantity} units of {inventory[sku]['Name']} to order.")
        
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")
    
    # Calculate order total
    total = 0
    for sku, quantity in supplier_orders[order_id]['items'].items():
        total += inventory[sku]['Price'] * quantity
    
    supplier_orders[order_id]['total'] = total
    print(f"\nOrder total: ${total:.2f}")
    print(f"Order {order_id} created successfully.")
    
    next_supplier_order_id += 1
    return order_id
def create_supplier_order():
    """Create a new supplier order"""
    global next_supplier_order_id
    
    print("\n***** Create Supplier Order *****\n")
    print("Available suppliers:")
    for supplier_id, supplier in suppliers.items():
        print(f"({supplier_id}) {supplier['name']} (Lead time: {supplier['lead_time']} days)")
    
    supplier_id = input("\nEnter supplier ID: ").upper()
    if supplier_id not in suppliers:
        print("Error: Invalid supplier ID.")
        return False
    
    order_id = f"SO{next_supplier_order_id:04d}"
    supplier_orders[order_id] = {
        'supplier': supplier_id,
        'items': {},
        'status': 'pending',
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'expected_delivery': (datetime.now() + timedelta(days=suppliers[supplier_id]['lead_time'])).strftime("%Y-%m-%d")
    }
    
    print(f"\nNew supplier order created: {order_id}")
    print(f"Supplier: {suppliers[supplier_id]['name']}")
    print(f"Expected delivery: {supplier_orders[order_id]['expected_delivery']}")
    
    while True:
        print("\nAdd items to order:")
        print("1. Add item")
        print("2. Finish order")
        choice = input("Enter your choice (1-2): ")
        
        if choice == "1":
            print("\nAvailable items:")
            for sku, item in inventory.items():
                print(f"({sku}) {item['Name']} - Current stock: {item['Stock']}")
            
            sku = input("\nEnter item SKU: ")
            if sku not in inventory:
                print("Error: Invalid item SKU.")
                continue
            
            try:
                quantity = int(input("Enter quantity to order: "))
                if quantity <= 0:
                    print("Error: Quantity must be positive.")
                    continue
            except ValueError:
                print("Error: Invalid quantity.")
                continue
            
            if sku in supplier_orders[order_id]['items']:
                supplier_orders[order_id]['items'][sku] += quantity
            else:
                supplier_orders[order_id]['items'][sku] = quantity
            
            print(f"Added {quantity} units of {inventory[sku]['Name']} to order.")
        
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")
    
    # Calculate order total
    total = 0
    for sku, quantity in supplier_orders[order_id]['items'].items():
        total += inventory[sku]['Price'] * quantity
    
    supplier_orders[order_id]['total'] = total
    print(f"\nOrder total: ${total:.2f}")
    print(f"Order {order_id} created successfully.")
    
    next_supplier_order_id += 1
    return order_id
def view_supplier_orders():
    """Display all supplier orders"""
    print("\n***** Supplier Orders *****\n")
    
    if not supplier_orders:
        print("No supplier orders found.")
        return
    
    for order_id, order in supplier_orders.items():
        print(f"\nOrder ID: {order_id}")
        print(f"Supplier: {suppliers[order['supplier']]['name']}")
        print(f"Status: {order['status']}")
        print(f"Date: {order['date']}")
        if order['status'] == 'delivered':
            print(f"Delivery Date: {order['delivery_date']}")
        else:
            print(f"Expected Delivery: {order['expected_delivery']}")
        
        print("\nItems:")
        total = 0
        for sku, quantity in order['items'].items():
            item_total = inventory[sku]['Price'] * quantity
            total += item_total
            print(f"{inventory[sku]['Name']}: {quantity} units @ ${inventory[sku]['Price']} each = ${item_total:.2f}")
        
        print(f"\nOrder Total: ${total:.2f}")
    
    print("\n")
from datetime import datetime, timedelta
from datetime import datetime, timedelta
from datetime import datetime, timedelta
# Supplier payment tracking
supplier_payments = {}  # Format: {payment_id: {'order_id': str, 'amount': float, 'status': 'pending/paid', 'date': date, 'payment_method': str}}
next_payment_id = 1
supplier_invoices = {}  # Format: {invoice_id: {'order_id': str, 'amount': float, 'due_date': date, 'status': 'pending/paid'}}
next_invoice_id = 1
# Supplier payment tracking
supplier_payments = {}  # Format: {payment_id: {'order_id': str, 'amount': float, 'status': 'pending/paid', 'date': date, 'payment_method': str}}
next_payment_id = 1
supplier_invoices = {}  # Format: {invoice_id: {'order_id': str, 'amount': float, 'due_date': date, 'status': 'pending/paid'}}
next_invoice_id = 1
def generate_supplier_invoice():
    """Generate an invoice for a supplier order"""
    global next_invoice_id
    
    print("\n***** Generate Supplier Invoice *****\n")
    
    if not supplier_orders:
        print("No supplier orders found.")
        return
    
    print("Pending supplier orders:")
    for order_id, order in supplier_orders.items():
        if order['status'] == 'delivered':
            print(f"{order_id} - {suppliers[order['supplier']]['name']} - Delivered on {order['delivery_date']}")
    
    order_id = input("\nEnter order ID to invoice: ").upper()
    if order_id not in supplier_orders or supplier_orders[order_id]['status'] != 'delivered':
        print("Error: Invalid or undelivered order.")
        return
    
    order = supplier_orders[order_id]
    invoice_id = f"INV{next_invoice_id:04d}"
    
    # Calculate invoice total
    total = 0
    for sku, quantity in order['items'].items():
        total += inventory[sku]['Price'] * quantity
    
    supplier_invoices[invoice_id] = {
        'order_id': order_id,
        'amount': total,
        'due_date': (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),  # 30 days payment terms
        'status': 'pending'
    }
    
    print(f"\nInvoice generated:")
    print(f"Invoice ID: {invoice_id}")
    print(f"Order ID: {order_id}")
    print(f"Supplier: {suppliers[order['supplier']]['name']}")
    print(f"Amount: ${total:.2f}")
    print(f"Due Date: {supplier_invoices[invoice_id]['due_date']}")
    
    next_invoice_id += 1
    return invoice_id
def generate_supplier_invoice():
    """Generate an invoice for a supplier order"""
    global next_invoice_id
    
    print("\n***** Generate Supplier Invoice *****\n")
    
    if not supplier_orders:
        print("No supplier orders found.")
        return
    
    print("Pending supplier orders:")
    for order_id, order in supplier_orders.items():
        if order['status'] == 'delivered':
            print(f"{order_id} - {suppliers[order['supplier']]['name']} - Delivered on {order['delivery_date']}")
    
    order_id = input("\nEnter order ID to invoice: ").upper()
    if order_id not in supplier_orders or supplier_orders[order_id]['status'] != 'delivered':
        print("Error: Invalid or undelivered order.")
        return
    
    order = supplier_orders[order_id]
    invoice_id = f"INV{next_invoice_id:04d}"
    
    # Calculate invoice total
    total = 0
    for sku, quantity in order['items'].items():
        total += inventory[sku]['Price'] * quantity
    
    supplier_invoices[invoice_id] = {
        'order_id': order_id,
        'amount': total,
        'due_date': (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),  # 30 days payment terms
        'status': 'pending'
    }
    
    print(f"\nInvoice generated:")
    print(f"Invoice ID: {invoice_id}")
    print(f"Order ID: {order_id}")
    print(f"Supplier: {suppliers[order['supplier']]['name']}")
    print(f"Amount: ${total:.2f}")
    print(f"Due Date: {supplier_invoices[invoice_id]['due_date']}")
    
    next_invoice_id += 1
    return invoice_id
def generate_supplier_invoice():
    """Generate an invoice for a supplier order"""
    global next_invoice_id
    
    print("\n***** Generate Supplier Invoice *****\n")
    
    if not supplier_orders:
        print("No supplier orders found.")
        return
    
    print("Pending supplier orders:")
    for order_id, order in supplier_orders.items():
        if order['status'] == 'delivered':
            print(f"{order_id} - {suppliers[order['supplier']]['name']} - Delivered on {order['delivery_date']}")
    
    order_id = input("\nEnter order ID to invoice: ").upper()
    if order_id not in supplier_orders or supplier_orders[order_id]['status'] != 'delivered':
        print("Error: Invalid or undelivered order.")
        return
    
    order = supplier_orders[order_id]
    invoice_id = f"INV{next_invoice_id:04d}"
    
    # Calculate invoice total
    total = 0
    for sku, quantity in order['items'].items():
        total += inventory[sku]['Price'] * quantity
    
    supplier_invoices[invoice_id] = {
        'order_id': order_id,
        'amount': total,
        'due_date': (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),  # 30 days payment terms
        'status': 'pending'
    }
    
    print(f"\nInvoice generated:")
    print(f"Invoice ID: {invoice_id}")
    print(f"Order ID: {order_id}")
    print(f"Supplier: {suppliers[order['supplier']]['name']}")
    print(f"Amount: ${total:.2f}")
    print(f"Due Date: {supplier_invoices[invoice_id]['due_date']}")
    
    next_invoice_id += 1
    return invoice_id
def view_supplier_payments():
    """Display supplier payment history"""
    print("\n***** Supplier Payment History *****\n")
    
    if not supplier_payments:
        print("No supplier payments found.")
        return
    
    for payment_id, payment in supplier_payments.items():
        print(f"\nPayment ID: {payment_id}")
        print(f"Order ID: {payment['order_id']}")
        print(f"Amount: ${payment['amount']:.2f}")
        print(f"Status: {payment['status']}")
        print(f"Date: {payment['date']}")
        print(f"Payment Method: {'Bank Transfer' if payment['payment_method'] == '1' else 'Check' if payment['payment_method'] == '2' else 'Credit Card'}")
    
    print("\n")
def view_supplier_payments():
    """Display supplier payment history"""
    print("\n***** Supplier Payment History *****\n")
    
    if not supplier_payments:
        print("No supplier payments found.")
        return
    
    for payment_id, payment in supplier_payments.items():
        print(f"\nPayment ID: {payment_id}")
        print(f"Order ID: {payment['order_id']}")
        print(f"Amount: ${payment['amount']:.2f}")
        print(f"Status: {payment['status']}")
        print(f"Date: {payment['date']}")
        print(f"Payment Method: {'Bank Transfer' if payment['payment_method'] == '1' else 'Check' if payment['payment_method'] == '2' else 'Credit Card'}")
    
    print("\n")
elif response == "6":
        print("\nWould you like to:")
        print("1. View order history")
        print("2. Request a refund")
        print("3. View inventory")
        print("4. Restock item")
        print("5. Check out-of-stock items")
        print("6. Create supplier order")
        print("7. Update supplier order status")
        print("8. View supplier orders")
        print("9. Generate supplier invoice")
        print("10. Process supplier payment")
        print("11. View supplier payment history")
        choice = input("Enter your choice (1-11): ")
        
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
        elif choice == "6":
            create_supplier_order()
        elif choice == "7":
            update_supplier_order_status()
        elif choice == "8":
            view_supplier_orders()
        elif choice == "9":
            generate_supplier_invoice()
        elif choice == "10":
            process_supplier_payment()
        elif choice == "11":
            view_supplier_payments()
    elif response == "12":
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

