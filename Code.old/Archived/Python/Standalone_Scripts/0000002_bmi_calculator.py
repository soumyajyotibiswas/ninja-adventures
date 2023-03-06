"""
User BMI Calculator
    input - Name
    input - Weight[kg]
    input - Height[m]

--@soumyajyotibiswas
"""

def calc_bmi(user_weight,user_height):
    return(round(user_weight/((user_height/100) ** 2),1))

def calc_user_bmi_standing(user_weight,user_height):
    bmi = calc_bmi(user_weight,user_height)
    if bmi < 18.5:
        result = "Underweight"
    elif bmi >= 18.5 and bmi <= 24.9:
        result = "Normal"
    elif bmi >= 25 and bmi <= 29.9:
        result = "Overweight"
    else:
        result = "Very overweight"
    return(f"Hello {user_name}. Your BMI is {bmi}. Your body mass index is {result}.")

def get_user_input():
    global user_name,user_weight,user_height
    user_name = input("Enter your name: ")
    user_weight = float(input("Enter your weight in Kg(s): "))
    user_height = float(input("Enter your height in cm(s): "))

def main():
    get_user_input()
    print(calc_user_bmi_standing(user_weight,user_height))

main()
