from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Union, Dict, List, Type, Any
json_type=Union[Dict[str, Any], List[Any], int, str, float, bool, Type[None]]

if TYPE_CHECKING:
    pass
import os,json
from datetime import datetime
from time import sleep

def introduce_delay():
    sleep(5)

# Global constants
EXECUTE_TIME=datetime.now().strftime("%d-%m-%Y %H:%M:%S")
COFFEE_MENU = {
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
RESOURCE_FILE_NAME=f'{os.path.dirname(os.path.realpath(__file__))}/memory_store.json'
RESOURCE_CONST={
    "water": {
        "Current_Level": 3000,
        "Lower_Limit": 500
    },
    "milk": {
        "Current_Level": 3000,
        "Lower_Limit": 500
    },
    "coffee": {
        "Current_Level": 1000,
        "Lower_Limit": 300
    },
    "money": 0
}
INTRO_MESSAGE=f'''


   _____ ____  ______ ______ ______ ______   _____      __     __
  / ____/ __ \|  ____|  ____|  ____|  ____| |  __ \   /\\ \   / /
 | |   | |  | | |__  | |__  | |__  | |__    | |  | | /  \\ \_/ / 
 | |   | |  | |  __| |  __| |  __| |  __|   | |  | |/ /\ \\   /  
 | |___| |__| | |    | |    | |____| |____  | |__| / ____ \| |   
  \_____\____/|_|    |_|    |______|______| |_____/_/    \_\_|
                                                                                                                                                                
Welcome to the coffee day machine.
Time: {EXECUTE_TIME}
'''
SYSTEM_MENU='''
1. Do you want to make coffee?
2. Do you want to print a report of current system?
3. Do you want to turn off the system?
4. Do you want to refill items, and take out money?
'''
INCORRECT_ATTEMPTS=5
TURN_OFF = False
MONEY_VALUE_CHART={
    'dollar':1,
    'quarter':0.25,
    'dime':0.10,
    'nickel':0.05,
    'penny':0.01
}

class CoffeeMachine():
    
    def __init__(self) -> None:
        self.TURN_OFF = TURN_OFF
        self.incorrect_attempts=INCORRECT_ATTEMPTS
        self.system_menu=SYSTEM_MENU
        self.coffee_menu=COFFEE_MENU
        self.resource_file_name = RESOURCE_FILE_NAME
        self.resources_constant = RESOURCE_CONST        
        self.initialize_resource_file()
        self.resources = self.load_from_resource_file()
        self.money_value_chart=MONEY_VALUE_CHART
        self.total_money = None

    def turn_on(self):
        print(INTRO_MESSAGE)

    def turn_off(self, value:bool):
        self.TURN_OFF = value

    def reset_machine(self):
        self.turn_off(False)

    def make_coffee(self,resources:json_type):
        options=self.print_options_for_coffee(resources)
        if len(options) == 0:
            raise Exception(f"Unable to provide any coffee options to user. Contact vendor for repair.")
        else:
            output=self.display_menu('coffee_choice',options)
            if output == False:
                raise Exception("Invalid choice made. System refreshing.")
        self.take_money(output)
        self.give_coffee(output)

    def print_options_for_coffee(self,resources:json_type)->list[Any]:
        options=[]
        for key in self.coffee_menu.keys():
            for ingredient in list(self.coffee_menu[key]['ingredients'].keys()):
                if (ingredient not in list(resources.keys())) or (self.coffee_menu[key]['ingredients'][ingredient] > resources[ingredient]['Current_Level']):
                    break
            options.append(key)
        return options

    def display_menu(self,when: str='',what: list[Any]=[]):
        count=0
        while(count < self.incorrect_attempts):
            if when=='initial':
                print(self.system_menu)
            if when=='coffee_choice':
                user_choice=input(f"Enter your choice, {what}: [eg: {what[0]}] --> ")
            else:
                user_choice=int(input(f"Enter your choice, {what}: [eg: {what[0]}] --> "))
            if self.is_correct_user_choice(user_choice=user_choice, choices=what):
                return user_choice
            else:
                count+=1
            if count == self.incorrect_attempts:
                break
        return False

    def is_correct_user_choice(self,user_choice:str, choices:json_type):
        if user_choice not in choices:
            return False
        else:
            return True
    
    def give_coffee(self,output:str):
        os.system('clear')
        self.print_current_resource_level(self.resources)
        introduce_delay()
        print(f"\nGetting your fresh {output} ready.")
        introduce_delay()
        print(f"Enjoy your {output}.\n")

    def take_money(self,choice:str):
        cost_of_choice=int(self.coffee_menu[choice]['cost'])
        print(f"\nYour '{choice}' will be a total of $'{cost_of_choice}'.")
        self.calculate_money(choice,cost_of_choice)

    def calculate_money(self,choice:str,cost_of_choice:float):
        print(f"\nYou can pay $'{cost_of_choice}' for {choice} using coins of {list(self.money_value_chart.keys())}, whose corresponding values are {list(self.money_value_chart.values())}")
        total=0
        for key in list(self.money_value_chart.keys()):
            total += round((int(input(f"\nEnter the '{key}' coins of value '{self.money_value_chart[key]}' you want. If you do not want to use '{key}' coins type 0 to got to next option: [eg: 0] --> "))) * self.money_value_chart[key],2)
            remaining=round(cost_of_choice - total,2)
            print(f"Total money entered till now is $'{total}'. Remaining needed for your choice is $'{remaining}'.\n")
        if total < cost_of_choice:
            print(f"You entered a total of $'{total}' which is less than the cost $'{cost_of_choice}' for your '{choice}'. Refunding $'{total}'.")
            raise Exception(f"Amount entered $'{total}' for '{choice}' is less than $'{cost_of_choice}'. System refreshing, refund provided.\n")
        elif total > cost_of_choice:
            print(f"You entered a total of $'{total}' which is more than the cost $'{cost_of_choice}' for your '{choice}'. Refunding $'{remaining}'. Proceeding to make coffee.\n")
        else:
            print(f"You entered a total of $'{total}' which is equal than the cost $'{cost_of_choice}' for your '{choice}'. Proceeding to make coffee.\n")
        input("\nEnter any key to continue..")
        self.update_current_resource_data(choice,cost_of_choice)

    def initialize_resource_file(self)->None:
        if not self.is_resource_file_present():
            self.write_to_resource_file(self.resources_constant)

    def is_resource_file_present(self) -> bool:
        if not (os.path.exists(self.resource_file_name)):
            return False
        return True

    def load_from_resource_file(self)->json_type:
        with open(self.resource_file_name,'r') as file:
            data=json.load(file)
            file.close()
        return data

    def is_enough_resources(self)->bool:
        for key in list(self.resources.keys()):
            if key.lower() != 'money':
                if self.resources[key]['Current_Level'] < self.resources[key]['Lower_Limit']:
                    return False
        return True

    def print_current_resource_level(self, data:json_type):
        print("\n****Generating System Report****")
        introduce_delay()
        for i in list(data.keys()):
            if i.lower() == 'coffee':
                print(f" '{i}' left {data[i]['Current_Level']}g.")
            elif i.lower() == 'money':
                print(f" The machine currently holds '${data[i]}'")
            else:
                print(f" '{i}' left {data[i]['Current_Level']}ml.")

    def write_to_resource_file(self, data:json_type)->None:
        with open(self.resource_file_name,'w') as file:
            file.write(json.dumps(data,indent=4))
            _ = file.close()

    def reset_resources(self)->None:
        print(f"\nDisplaying pre reset status below:")
        self.print_current_resource_level(self.resources)
        self.resources = self.resources_constant
        self.write_to_resource_file(self.resources)
        print(f"\nMachine re-filled and money withdrawn.")
        print(f"\nDisplaying post reset status below:")
        self.print_current_resource_level(self.resources)

    def update_current_resource_data(self,choice:str,cost_of_choice:float):
        if 'money' in list(self.resources.keys()):
            self.resources['money'] = self.resources['money'] + cost_of_choice
        else:
            self.resources.update({'money':cost_of_choice})
        for ingredient in list(COFFEE_MENU[choice]['ingredients'].keys()):
            self.resources[ingredient]['Current_Level'] -= COFFEE_MENU[choice]['ingredients'][ingredient]
        self.write_to_resource_file(self.resources)
