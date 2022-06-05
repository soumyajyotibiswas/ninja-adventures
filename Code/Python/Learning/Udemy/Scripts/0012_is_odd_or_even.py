# Returns odd / even for a number

user_input=int(input("Enter an integer of your choice: "))
if user_input % 2 == 0:
    print(f"{user_input} is an even number.")
else:
    print(f"{user_input} is an odd number.")