user_height=float(input("Enter height in m: "))
user_weight=float(input("Enter weight in kg: "))
bmi=round(user_weight/user_height**2,1)
print(f"Your body mass index is: {bmi}")
if bmi < 18.5:
    print("You are underweight.")
elif bmi >= 18.5 and bmi < 25:
    print("You have a normal BMI.")
elif bmi >= 25 and bmi < 30:
    print("You are obese.")
else:
    print("Bruh! What you doing? Start working out immediately.")