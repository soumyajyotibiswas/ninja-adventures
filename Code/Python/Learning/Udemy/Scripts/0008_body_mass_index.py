user_height=float(input("Enter height in m: "))
user_weight=float(input("Enter weight in kg: "))
bmi=round(user_weight/user_height**2,1)
print(f"Your body mass index is: {bmi}")