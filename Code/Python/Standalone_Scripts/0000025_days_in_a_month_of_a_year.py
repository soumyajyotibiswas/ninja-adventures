def is_leap_year(year:int):
    """Tells us if the year is a leap year or not.
    Returns True / False

    Args:
        year (int): Provide the year for which you want to know
                    if it is leap year or not.
    """
    if year % 4 == 0:
        if year % 100 == 0 and year % 400 != 0:
            return False
        else:
            return True
    else:
        return False

def return_days_of_month(month:int,year:int):
    """Returns the number of days in a month.

    Args:
        month (str): Enter the month you want to check.
    """
    days_in_month=[31,28,31,30,31,30,31,31,30,31,30,31]
    leap_year=is_leap_year(year)
    if leap_year and month == 2:
        return (days_in_month[month-1]+1)
    else:
        return (days_in_month[month-1])

def check_input_month(month:int):
    """Checks the month that the user provided as input

    Args:
        month (int): This is the input month

    Returns:
        bool: Returns True if the input month is correct and False if incorrect
    """
    if month > 12 or month < 1:
        return False
    else:
        return True

def main():
    print("""
    Welcome to the days in a month of a year program.
    The program will tell you for a year that you enter and the month
    how many days are there in that month.    
    """)
    year=int(input("Enter the year you want to check: [eg:1990] "))
    month=int(input("Enter the month you want to check, use numbers from 1 to 12: [eg:1 for January, 2 for February] "))
    if not check_input_month(month):
        print(f"The month you entered '{month}' is not a valid choice.")
        return
    days=return_days_of_month(month,year)
    print(f"Number of days in month '{month}' of year '{year}' is '{days}'.")

main()


    