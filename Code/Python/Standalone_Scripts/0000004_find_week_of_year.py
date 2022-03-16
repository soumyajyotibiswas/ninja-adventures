"""
Find week of year from a given date string
    -- user_input : date_string
    -- date_string format: dd/mm/yyyy (date/month/year) | Example: 01/12/2001

--@soumyajyotibiswas
"""

import datetime

date_string_format = '''
Valid date string format provided below
date_string format: dd/mm/yyyy (date/month/year) | Example: 01/12/2001

Press enter to continue
'''

def get_user_input():
    return(input("\nEnter date string | dd/mm/yyyy (date/month/year) | Example: 01/12/2001 : "))

def return_week_of_year(date_string):
    return((datetime.datetime.strptime(date_string, '%d/%m/%Y')).isocalendar().week)

def main():
    user_input = get_user_input()
    try:
        week_of_year = return_week_of_year(user_input)
        print(f"\nWeek of year for the provided date {user_input} is {week_of_year}")
    except ValueError:
        print("\nInvalid input !!! See valid format.")
        print(f"\n{date_string_format}")
    except:
        print("Unknown exception. Terminating.")

main()