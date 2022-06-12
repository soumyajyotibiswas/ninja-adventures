import os,json
from datetime import datetime
from time import sleep

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
    }
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
PRE_CHECK='''
Turning on machine. 
Running prechecks.
System is loading.
Please wait.
'''
SYSTEM_MENU='''
1. Do you want to make coffee?
2. Do you want to print a report of current system?
3. Do you want to turn off the system?
4. Do you want to refill items, and take out money?
'''
INCORRECT_ATTEMPS=5

def is_resource_file_present():
    if not (os.path.exists(RESOURCE_FILE_NAME)):
        write_to_resource_file(RESOURCE_CONST)
    return True

def load_from_resource_file():
    with open(RESOURCE_FILE_NAME,'r') as file:
        data=json.load(file)
        file.close()
    return data

def check_resource_level(data):
    for key in list(data.keys()):
        if key.lower() != 'money':
            if data[key]['Current_Level'] < data[key]['Lower_Limit']:
                return False
    return True

def print_current_resource_level(data):
    print("\n****Generating System Report****")
    introduce_delay()
    for i in list(data.keys()):
        if i.lower() == 'coffee':
            print(f"'{i}' left {data[i]['Current_Level']}g.")
        elif i.lower() == 'money':
            print(f"The machine currently holds '${data[i]}'")
        else:
            print(f"'{i}' left {data[i]['Current_Level']}ml.")

def write_to_resource_file(data):
    with open(RESOURCE_FILE_NAME,'w') as file:
        file.write(json.dumps(data,indent=4))
        _ = file.close()

def is_correct_user_choice(user_choice, choices):
    if user_choice not in choices:
        return False
    else:
        return True

def display_menu(when='',what=''):
    count=0
    while(count < 5):
        if when=='initial':
            print(SYSTEM_MENU)
        if when=='coffee_choice':
            user_choice=input(f"Enter your choice, {what}: [eg: {what[0]}] --> ")
        else:
            user_choice=int(input(f"Enter your choice, {what}: [eg: {what[0]}] --> "))
        if is_correct_user_choice(user_choice, what):
            return user_choice
        else:
            count+=1
        if count == INCORRECT_ATTEMPS:
            break
    return False

def introduce_delay():
    sleep(5)


