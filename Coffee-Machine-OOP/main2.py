from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine
from menu import MenuItem, Menu

def main():
    coffee_maker = CoffeeMaker()
    money_machine = MoneyMachine()

    is_on = True
    while is_on:
        options = Menu().get_items()
        choice = input(f"What would you like? ({options}) ").lower()
        if choice == "off":
            is_on = False
        elif choice == "report":
            coffee_maker.report()
            money_machine.report()
        elif choice not in options.split("/"):
            print(f"Sorry, we don't offer {choice}.")
        else:
            drink = Menu().find_drink(choice)
            is_resource_sufficient = coffee_maker.is_resource_sufficient(drink)
            is_enough_money = money_machine.make_payment(drink.cost)
            if is_resource_sufficient and is_enough_money:
                coffee_maker.make_coffee(drink)


if __name__ == "__main__":
    main()
