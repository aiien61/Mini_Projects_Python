from data import MENU, resources

profit = 0

def place_order() -> str:
    return input("What would you like? (espresso/latte/cappuccino/): ").lower()

# print report
def print_report(resources: dict) -> None:
    print(f"Water: {resources['water']}ml")
    print(f"Milk: {resources['milk']}ml")
    print(f"Coffee: {resources['coffee']}g")
    print(f"Money: ${profit}")

# check resources sufficient
def is_resource_sufficient(order_ingredients: dict) -> bool:
    """Returns True when order can be made, False if ingredients are insufficient."""

    is_enough = True
    for item, required_amount in order_ingredients.items():
        if resources[item] < required_amount:
            print(f"Sorry there is not enough {item}.")
            is_enough = False
    return is_enough

# process coins
def process_coins() -> float:
    """Returns the total calculated from coins inserted."""

    print("Please insert coins.")
    total = 0
    total += int(input("how many quarters?: ")) * 0.25
    total += int(input("how many dimes?: ")) * 0.1
    total += int(input("how many nickles?: ")) * 0.05
    total += int(input("how many pennies?: ")) * 0.01
    return total

# check transaction successful
def is_transaction_successful(money_received: float, drink_cost: float) -> bool:
    """Returns True when the payment is accepted, or False if money is insufficient."""

    if money_received < drink_cost:
        print("Sorry that's not enough money. Money refunded.")
        return False

    global profit
    profit += drink_cost

    change = round(money_received - drink_cost, 2)
    print(f"Here is ${change} in change.")
    return True
    
    
# make coffee
def make_coffee(drink_name: str, order_ingredients: dict) -> None:
    """Deduct the required ingredients from the resources."""
    for item, amount in order_ingredients.items():
        resources[item] -= amount
    print(f"Here is your {drink_name} ☕. Enjoy!")
    return None
    

def main():
    print("Welcome to the coffee machine!")
    while True:
        choice = place_order()
        if choice == "off":
            print("Goodbye!")
            break

        if choice == "report":
            print_report(resources)
            continue

        drink = MENU[choice]
        if not is_resource_sufficient(drink['ingredients']):
            continue
        
        payment = process_coins()
        if not is_transaction_successful(payment, drink['cost']):
            continue

        make_coffee(choice, drink['ingredients'])

if __name__ == "__main__":
    main()