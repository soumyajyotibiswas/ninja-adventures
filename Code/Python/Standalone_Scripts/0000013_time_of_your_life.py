from datetime import datetime,timedelta
intro_message="""
Welcome to the age in weeks calculator.
This program tells you how many weeks you have left in your life, if you were to live till 100 years of age.
You will have to enter your date of birth in the format month/day/year[mm/dd/yyyy] and the program will tell you, your current age, years left till your age is 100, weeks left till your age is 100.
Assumptions:
1yr = 365days
1yr = 52weeks
"""
print(intro_message)
user_dob=datetime.strptime(input("Enter your date of birth in the format month/day/year[mm/dd/yyyy]: "),'%m/%d/%Y')
current_date=datetime.now()
year_when_100=user_dob + timedelta(days=36500)
weeks_left_till_100 = round((year_when_100 - current_date).days / 7,1)
years_left_till_100 = round((year_when_100 - current_date).days / 365,1)
current_age = round((current_date - user_dob).days / 365,1)
print(f"Your current age in years is {current_age}, you have {years_left_till_100} years and {weeks_left_till_100} weeks left till you are 100 years old.")