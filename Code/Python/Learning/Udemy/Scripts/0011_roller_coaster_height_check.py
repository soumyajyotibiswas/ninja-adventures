# If else statment example

user_height=int(input("Welcome to the roller coaster.\nTell me your height in cm: "))
if user_height > 120:
    user_age=int(input("What is your age?: "))
    print("You are tall enough for the ride.")
    if user_age < 12:
        print("You have to pay $5 for the ride.")
    elif user_age >= 12 and user_age < 18:
        print("You have to pay $7 for the ride.")
    else:
        print("You have to pay $10 for the ride.")
else:
    print("Sorry but you do not meet the height requirements for the ride.")