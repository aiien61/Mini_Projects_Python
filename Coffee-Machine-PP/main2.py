from data import MENU, resources

def is_sufficient(ingredients: str):
    for item, amount in ingredients.items():
        if resources[item] < amount:
            print(f"Sorry, there is not enough {item}")
            return False
    return True


def show_report(profit: float):
    print(f"Water: {resources['water']}ml")
    print(f"Milk: {resources['milk']}ml")
    print(f"Coffee: {resources['coffee']}g")
    print(f"Money: ${profit}")


def process_coins() -> float:
    print("Please insert coins.")
    total = 0
    total += int(input("how many quarters?: ")) * 0.25
    total += int(input("how many dimes?: ")) * 0.1
    total += int(input("how many nickles?: ")) * 0.05
    total += int(input("how many pennies?: ")) * 0.01
    return total


def is_transaction_successful(cost: str, money_received: float, profit_holder: dict):
    change = money_received - cost
    if money_received < cost:
        print("Sorry, there's not enough money. Money refunded.")
        return False

    profit_holder["profit"] += cost
    change = round(money_received - cost, 2)
    if change > 0:
        print(f"Here is ${change} dollars in change.")

    return True

def make_coffee(drink_name, drink_ingredients):
    for ingredient, amount in drink_ingredients.items():
        resources[ingredient] -= amount
    print(f"Here is your {drink_name} ☕. Enjoy!")
    return None
    

def main():
    profit_holder = {"profit": 0}
    is_on = True
    while is_on:
        choice = input("What would you like? (espresso/latte/cappuccino): ")
        order = choice.lower()
        if order == "off":
            is_on = False
        elif order == "report":
            show_report(profit_holder["profit"])
        elif order not in MENU.keys():
            print(f"Sorry, we don't offer {order}.")
        else:
            drink = MENU[order]
            if not is_sufficient(drink["ingredients"]):
                continue

            payment = process_coins()
            if is_transaction_successful(drink["cost"], payment, profit_holder):
                make_coffee(order, drink["ingredients"])


if __name__ == "__main__":
    main()