# Import classes and modules
from CoffeeMachine import CoffeeMachine
from CoffeeMachine import introduce_delay,sleep
import os
coffee_machine=CoffeeMachine()
PRE_CHECK='''
Turning on machine. 
Running pre-checks.
System is loading.
Please wait.
'''
MENU_ACTIONS={
    1:coffee_machine.make_coffee,
    2:coffee_machine.print_current_resource_level,
    3:coffee_machine.turn_off,
    4:coffee_machine.reset_resources
}
def main():
    try:
        ## Machine Pre-check
        print(PRE_CHECK)
        introduce_delay()
        if not coffee_machine.is_enough_resources():
            raise Exception("Resource level below threshold. Kindly refill resource. Contact vendor.")

        ## Machine turn on
        coffee_machine.turn_on()
        while(True):
            input("\nEnter any key to continue..")
            os.system('clear')
            ### Display coffee machine menu
            output=coffee_machine.display_menu(when='initial',what=list(MENU_ACTIONS.keys()))
            if output == False:
                os.system('clear')
                print(f"\nYou made '{coffee_machine.incorrect_attempts}' wrong attempts while selecting an option from system menu. Machine will lock for 60 seconds.")
                sleep(60)
            else:
                if output == 1 or output == 2:
                    MENU_ACTIONS[output](coffee_machine.resources)
                elif output == 3:
                    MENU_ACTIONS[output](True)
                else:
                    MENU_ACTIONS[output]()
            if coffee_machine.TURN_OFF:
                os.system('clear')
                print("\nMachine shutting down. Goodbye.")
                coffee_machine.write_to_resource_file(coffee_machine.resources)
                introduce_delay()
                break
    except Exception as e:
        print(e)

main()