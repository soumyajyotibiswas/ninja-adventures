def print_intro():
    intro_message="""
     _____________________
    |  _________________  |
    | | 12           0. | |
    | |_________________| |
    |  ___ ___ ___   ___  |
    | | 7 | 8 | 9 | | + | |
    | |___|___|___| |___| |
    | | 4 | 5 | 6 | | - | |
    | |___|___|___| |___| |
    | | 1 | 2 | 3 | | * | |
    | |___|___|___| |___| |
    | | . | 0 | = | | / | |
    | |___|___|___| |___| |
    |_____________________|

    Welcome to the simple calulator. The program helps you 
    perform simple arithmatic calculations.
    """
    print(intro_message)

def add_two_entries(x1:float,x2:float):
    return(x1+x2)

def substract_two_entries(x1:float,x2:float):
    return(x1-x2)

def divide_two_entries(x1:float,x2:float):
    return(x1/x2)

def multiply_two_entries(x1:float,x2:float):
    return(x1*x2)

def arithmatic_operations(x1:float,x2:float,operator:str):
    """Calls the underlying operation functions.

    Args:
        x1 (float): First number.
        x2 (float): Second number.
        operator (str): Operation type.

    Returns:
        float | str: e1: operator not defined. e2: division by 0.
    """
    operations_dict={
        '+':add_two_entries(x1,x2),
        '-':substract_two_entries(x1,x2),
        '/':divide_two_entries(x1,x2),
        '*':multiply_two_entries(x1,x2)
    }
    if operator not in operations_dict.keys():
        return 'e1'
    elif x2 == 0 and operator == '/':
        return 'e2'
    else:
        return operations_dict[operator]

def main():
    print_intro()
    result=0
    x1=float(input("Enter the first number: "))
    while(True):        
        x2=float(input("Enter the next number: "))
        operator=input("Enter the operation you want to perform: [eg: + - * /] ")            
        result = (arithmatic_operations(x1,x2,operator))
        if result == 'e1':
            print(f"The operator '{operator}' is not defined. Try again!")
            return
        elif result == 'e2':
            print(f"The operation between '{x1}' '{operator}' '{x2}' will result in an error 'ZeroDivisionError: float division by zero'. You cannot divide a number by 0. Try again!")
            return
        to_continue=input(f"The result of '{x1}' '{operator}' '{x2}' is '{result}'. Do you want to continue performing operations on '{result}? To continue type in 'yes': [eg: yes] ").lower()
        if to_continue != 'yes':
            to_exit=input(f"To exit just type in exit: [eg: exit] ").lower()
            if to_exit == 'exit':
                print(f"Final result is '{result}'.")
                break
            input(f"Final result is '{result}'. Starting a new instance of the calulator. Press any key to continue.")
            main()
        else:
            x1=result
        
main()
