from data import MENU, resources


def is_resource_sufficient(order_ingredients: dict) -> bool:
    """
    Returns True when order can be made, False if ingredients are insufficient.
    """
    for item in order_ingredients:
        if resources[item] < order_ingredients[item]:
            print(f"Sorry there is not enough {item}.")
            return False
    return True


def process_coins() -> float:
    """Returns the total calculated from coins inserted."""
    print("Please insert coins.")
    total = int(input("how many quarters?: ")) * 0.25
    total += int(input("how many dimes?: ")) * 0.1
    total += int(input("how many nickles?: ")) * 0.05
    total += int(input("how many pennies?: ")) * 0.01    
    return total


def is_transaction_successful(money_received: float,
                              drink_cost: float,
                              profit_holder: list) -> bool:
    """Returns True when the payment is accepted, or False if money is 
    insufficient.
    """
    if money_received >= drink_cost:
        change = round(money_received - drink_cost, 2)
        print(f"Here is ${change} in change.")

        profit_holder[0] += drink_cost
        return True
    else:
        print("Sorry that's not enough money. Money refunded.")
        return False


def make_coffee(drink_name: str, order_ingredients: dict) -> None:
    for item in order_ingredients:
        resources[item] -= order_ingredients[item]
    print(f"Here is your {drink_name} ☕. Enjoy!")
    return None
    

def coffee_machine():
    profit_holder = [0]
    is_on = True
    while is_on:
        choice = input("What would you like? (espresso/latte/cappuccino): ")
        if choice == "off":
            is_on = False
        elif choice == "report":
            print(f"Water: {resources['water']}ml.")
            print(f"Milk: {resources['milk']}ml")
            print(f"Coffee: {resources['coffee']}g")
            print(f"Money: ${profit_holder[0]}")
        else:
            drink = MENU[choice]
            if is_resource_sufficient(drink['ingredients']):
                payment = process_coins()
                if is_transaction_successful(payment, drink['cost'], profit_holder):
                    make_coffee(choice, drink['ingredients'])

coffee_machine()

