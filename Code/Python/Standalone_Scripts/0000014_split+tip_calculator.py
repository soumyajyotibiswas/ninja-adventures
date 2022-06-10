intro_message="""
Welcome to the split and tip calculator.
The program will tell you how much your share with the tip added is.
"""
print(intro_message)
total_bill=float(input("What is the total bill? $"))
split_by=int(input("How many people to split the bill between? "))
tip_percentage=int(input("How much you want to tip? 10,15, or 20%? "))
split_amount=round((total_bill*(1+(tip_percentage/100)))/split_by,2)
print(f"Each person has to pay ${split_amount}.")