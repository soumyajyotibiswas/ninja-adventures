intro_message="""
Welcome to the leap year program.
This program tells you if the year is a leap year or not
A leap year is divisible by 4, but not divisible by 100, except
the ones divisible by 400
"""
print(intro_message)
user_input=int(input("Enter the year of your choice: "))
leap_year_message=f"The year {user_input} is a leap year."
not_leap_year_message=f"The year {user_input} is not a leap year."
if user_input % 4 == 0:
    if user_input % 100 == 0 and not user_input % 400 == 0:
        print(not_leap_year_message)
    else:
        print(leap_year_message)
else:
    print(not_leap_year_message)