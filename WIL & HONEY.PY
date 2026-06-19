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
    
def checkout():
    print("\n****Checkout****\n")
    view_cart()
    print("Thank you for shopping with WIL & HONEY!!!!!")
    print("\n")

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

