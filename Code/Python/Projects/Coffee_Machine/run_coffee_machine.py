import common_config as cc

# Global constants
TURN_OFF=False
RESOURCE_DATA=''
MASTER_INCORRECT_ATTEMPTS=5

# Functions
def resource_data_refresh_from_file():
    global RESOURCE_DATA
    RESOURCE_DATA=cc.load_from_resource_file()

def resource_prechecks():
    if cc.is_resource_file_present():
        resource_data_refresh_from_file()
        if not cc.check_resource_level(RESOURCE_DATA):
            cc.print_current_resource_level(RESOURCE_DATA)
            raise Exception("Resource level below threshold. Kindly refill resource. Contact vendor.")
    else:
        raise Exception(f"Resource file missing. Cannot proceed with operation. Check if {cc.RESOURCE_FILE_NAME} is present.")

def turn_off_machine():
    global TURN_OFF
    TURN_OFF = True

def update_report():
    if RESOURCE_DATA == '':
        resource_data_refresh_from_file()
    else:
        cc.write_to_resource_file(RESOURCE_DATA)
    cc.print_current_resource_level(RESOURCE_DATA)

def make_coffee():
    options=print_options_for_coffee()
    if len(options) == 0:
        update_report()
        raise Exception(f"Unable to provide any coffee options to user. Contact vendor for repair.")
    else:
        output=cc.display_menu('coffee_choice',options)
        if output == False:
            raise Exception("Invalid choice made. System refreshing.")
    take_money(output)
    give_coffee(output)
    resource_prechecks()

def print_options_for_coffee():
    options=[]
    for key in cc.COFFEE_MENU.keys():
        for ingredient in list(cc.COFFEE_MENU[key]['ingredients'].keys()):
            if (ingredient not in list(RESOURCE_DATA.keys())) or (cc.COFFEE_MENU[key]['ingredients'][ingredient] > RESOURCE_DATA[ingredient]['Current_Level']):
                break
        options.append(key)
    return options

def take_money(choice):
    cost_of_choice=int(cc.COFFEE_MENU[choice]['cost'])
    print(f"\nYour '{choice}' will be a total of $'{cost_of_choice}'.")
    count_money(cost_of_choice,choice)

def count_money(cost_of_choice,choice):
    value_chart={
        'dollar':1,
        'quarter':0.25,
        'dime':0.10,
        'nickel':0.05,
        'penny':0.01
    }
    print(f"\nYou can pay $'{cost_of_choice}' for {choice} using coins of",*list(value_chart.keys()))
    total=0
    for key in list(value_chart.keys()):
        total += round((int(input(f"Enter the '{key}' coins of value '{value_chart[key]}' you want. If you do not want to use '{key}' coins type 0 to got to next option: [eg: 0] --> "))) * value_chart[key],2)
        remaining=round(cost_of_choice - total,2)
        print(f"Total money entered till now is $'{total}'. Remaining needed for your choice is $'{remaining}'.\n")
    if total < cost_of_choice:
        print(f"You entered a total of $'{total}' which is less than the cost $'{cost_of_choice}' for your '{choice}'. Refunding $'{total}'.")
        raise Exception(f"Amount entered $'{total}' for '{choice}' is less than $'{cost_of_choice}'. System refreshing, refund provided.\n")
    elif total > cost_of_choice:
        print(f"You entered a total of $'{total}' which is more than the cost $'{cost_of_choice}' for your '{choice}'. Refunding $'{remaining}'. Proceeding to make coffee.\n")
    else:
        print(f"You entered a total of $'{total}' which is equal than the cost $'{cost_of_choice}' for your '{choice}'. Proceeding to make coffee.\n")
    update_current_resource_data(choice,cost_of_choice)

def update_current_resource_data(choice,cost_of_choice):
    global RESOURCE_DATA
    if 'money' in list(RESOURCE_DATA.keys()):
        RESOURCE_DATA['money'] = RESOURCE_DATA['money'] + cost_of_choice
    else:
        RESOURCE_DATA.update({'money':cost_of_choice})
    for ingredient in list(cc.COFFEE_MENU[choice]['ingredients'].keys()):
        RESOURCE_DATA[ingredient]['Current_Level'] -= cc.COFFEE_MENU[choice]['ingredients'][ingredient]
    update_report()

def give_coffee(output):
    print(f"\nGetting your fresh {output} ready.")
    cc.introduce_delay()    
    print(f"Enjoy your {output}.\n")

def refill_and_take_money():
    cc.write_to_resource_file(cc.RESOURCE_CONST)
    print(f"\nMachine re-filled and money withdrawn.")

# Menu action mapping
MENU_ACTIONS={
    1:make_coffee,
    2:update_report,
    3:turn_off_machine,
    4:refill_and_take_money
}

def main():
    try:
        cc.os.system('clear')
        print(cc.PRE_CHECK)
        cc.introduce_delay()
        resource_prechecks()
        print(cc.INTRO_MESSAGE)
        while(True):
            input("\nEnter any key to continue..")
            cc.os.system('clear')
            output=cc.display_menu(when='initial',what=list(MENU_ACTIONS.keys()))
            if output == False:
                print(f"You made '{cc.INCORRECT_ATTEMPS} while selecting an option from system menu. Machine will lock for 60 seconds.'")
                cc.sleep(60)
            else:
                MENU_ACTIONS[output]()
            if TURN_OFF:
                print("Machine shutting down. Goodbye.")
                cc.write_to_resource_file(RESOURCE_DATA)
                break
    except Exception as e:
        print(e)

main()