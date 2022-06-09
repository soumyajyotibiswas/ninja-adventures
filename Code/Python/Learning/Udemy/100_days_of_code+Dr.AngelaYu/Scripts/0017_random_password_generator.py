import random, string
# Program variable
intro_message='''
Welcome to the random password generator.
This program generates alpha-numeric passwords
with symbols added to it.
The minimum password length is 8, and maximum is 16.
'''
letters_list=string.ascii_letters
symbol_list="~!@#$%^&*_-+=`|\(){}[]:;\"'<>,.?/"
numbers_list=list(range(1,10))

# Program start
print(intro_message)
password_length=int(input("Enter the length of the password you want to generate: "))
if password_length < 8:
    print(f"The length of password specified is {password_length}, which is less than the minimum length of 8. Try generating a password of greater length for best security.")
elif password_length > 16:
    print(f"The length of password specified is {password_length}, which is more than the maximum length of 16. Try generating a password of length less than or equal to 16.")
else:
    sequence_of_letters_or_numbers=int(round(password_length / 3,0))
    sequence_of_symbols=int(password_length-(2*sequence_of_letters_or_numbers))
    letters=random.choices(letters_list,k=sequence_of_letters_or_numbers)
    numbers=random.choices(numbers_list,k=sequence_of_letters_or_numbers)
    symbols=random.choices(symbol_list,k=sequence_of_symbols)
    password=letters+numbers+symbols
    random.shuffle(password)
    print("Your password is -->16",''.join(map(str,password)))
