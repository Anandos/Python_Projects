MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 600,
    "milk": 400,
    "coffee": 250,
}

money = 0

art = """
      )  (
     (   ) )
      ) ( (
    _______)_
 .-'---------|  
( C|/\/\/\/\/|
 '-./\/\/\/\/|
   '_________'
    '-------'"""

# get user input for order /
# output behaviour if not coffee /
# check resources has enough for user coffee order /
# if so, deplete resources
# ask user for cash amount
# check cash input total
# give change or ask for more
# add money input to resources
# deliver coffee


def process_input():
    """prompt and process user input for coffe order or anything else,
    only exits to turn off or a coffee order"""
    if user_order == "off":
        print("Coffee Machine shutting down...")
        exit()
    elif user_order == "report":
        print(f"Water: {resources['water']}ml")
        print(f"Coffee: {resources['coffee']}g")
        print(f"Milk: {resources['milk']}ml")
        print(f"Money: ${money:.2f}\n")
    elif user_order in MENU:
        print("Checking resources for your order...")
        return MENU[user_order]
    else:
        print("Sorry, user input invalid, try again...")


def process_coins():
    """prompt and process user input of money, and return total"""
    user_coins = int(input("How many quarters? ")) * 0.25
    user_coins += int(input("How many dimes? ")) * 0.10
    user_coins += int(input("How many nickels? ")) * 0.05
    user_coins += int(input("How many pennies? ")) * 0.01
    return user_coins


def deplete_resources(resources):
    for item in order["ingredients"]:
        resources[item] -= order['ingredients'][item]
        # print(f"{resources[item]} -= {order['ingredients'][item]}")
    return resources


while True:
    order = {}
    user_order = ""
    machine_status = True
    while user_order not in MENU: #while input is not coffee order
        user_order = input("Please type your order (espresso/latte/cappuccino)\n")
        order = process_input()  # return dictionary coffee to 'order'
    print(f"order: {user_order} {order}")

    sufficient_resources = True
    for item in order["ingredients"]:
        if order["ingredients"][item] <= resources[item]:
            print(f"{item} sufficient")
        else:
            print(f"{item} insufficient\n")
            sufficient_resources = False

    if sufficient_resources:
        print(f"\nPrice for {user_order} is ${order['cost']:.2f}")
        payment = process_coins()
        if payment >= order['cost']:
            print("Thank you, here is your change")
            change = payment - order['cost']
            money += order['cost']
            print(f"${change:.2f}")

        # deplete resources
        deplete_resources(resources)
        print(f"\nResources now at {resources}")
        # deliver coffee
        print(f"\nHere is your {user_order} ☕️, enjoy\n")
