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
    
    