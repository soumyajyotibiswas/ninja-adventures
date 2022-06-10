import string, os

def alphabet_list_lower():
    return(list(string.ascii_lowercase))

def alphabet_list_upper():
    return(list(string.ascii_uppercase))

def number_list():
    return(list(range(0,10)))

def symbol_list():
    return(list("~!@#$%^&*_-+=`|\(){}[]:;\"'<>,.?/ "))

def shift_input_by(input,shift_by,operation_type):
    if input.isnumeric():
        input=int(input)
        input_list_full=number_list()
    elif input.isalpha():
        if input.islower():
            input_list_full=alphabet_list_lower()
        else:
            input_list_full=alphabet_list_upper()
    elif input in symbol_list():
        input_list_full=symbol_list()      
    else:
        raise Exception(f"'{input}' is an unknown data type. Cannot proceed with '{operation_type}' operation.")
    input_list_full_size=len(input_list_full) - 1
    index=input_list_full.index(input)
    if shift_by > input_list_full_size:
        shift_by = shift_by % input_list_full_size
    if operation_type == 'encode':
        if index + shift_by > input_list_full_size:
            index=index + shift_by - input_list_full_size - 1
        else:
            index=index + shift_by
    else:
        index=index - shift_by
    return(str(input_list_full[index]))

def perform_cipher_op(user_input,user_operation,user_step_by):
    return(''.join([shift_input_by(input=x,shift_by=user_step_by,operation_type=user_operation) for x in list(user_input)]))

def static_intro():
    print('''
    Welcome to the secrect cipher program.
    This program will help you encode/decode
    your alphanumeric strings. Security before
    everything.
    ''')

def main():
    while(True):
        os.system('clear')
        static_intro()
        user_input=input("Enter the string convert: ")
        user_operation=input("Do you want to encode / decode? ")
        user_step_by=int(input("Enter the step displacement size: "))
        coded_cipher=perform_cipher_op(user_input=user_input,user_operation=user_operation,user_step_by=user_step_by)
        print(coded_cipher)
        do_continue=(input("Do you want to continue creating ciphers? Type in yes or no: ")).lower()
        if do_continue != 'yes':
            break

main()
