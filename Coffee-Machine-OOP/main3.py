from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

def place_order(menu: Menu) -> str:
    options: str = menu.get_items()
    return input(f"What would you like? ({options}): ").lower()

def main():
    print("Welcome to the Coffee Machine!")
    money_machine: MoneyMachine = MoneyMachine()
    coffee_maker: CoffeeMaker = CoffeeMaker()
    menu: Menu = Menu()

    is_on: bool = True

    while is_on:
        choice: str = place_order(menu)
        if choice == "off":
            print("Goodbye!")
            is_on = False
            continue

        if choice == "report":
            coffee_maker.report()
            money_machine.report()
            continue
        
        drink = menu.find_drink(choice)
        if not coffee_maker.is_resource_sufficient(drink):
            continue

        if not money_machine.make_payment(drink.cost):
            continue
        
        coffee_maker.make_coffee(drink)

if __name__ == "__main__":
    main()
