intro_message="""
Hey! Welcome to Crazy Pizza.
Our ordering system is completely online. 
You can select from the menu and order your custom pizza.
"""
print(intro_message)
pizza_sizes={'small':5,'medium':10,'large':15}
govt_tax = 2
topping_price = 3
user_input_pizza_size=input("Do you want a small / medium or large pizza?: [SMALL | MEDIUM | LARGE]\n").lower()
if user_input_pizza_size in pizza_sizes.keys():
    print(f"The pizza size your chose is '{user_input_pizza_size}'.")
    user_topping = input("You can add chicken as your topping on your pizza. Do you want it? [YES | NO]\n").lower()
    if user_topping not in ['yes','no']:
        print(f"The answer '{user_topping}' you provided to add a topping to your pizza is not valid. Choose either Yes or no. Try again!.")
    else:
        bill_breakup=f"""
        Item                                            Cost($)
        {user_input_pizza_size.capitalize()} size pizza                                {pizza_sizes[user_input_pizza_size]}
        Tax                                             {govt_tax}
        """
        if user_topping == 'yes':
            bill = topping_price + pizza_sizes[user_input_pizza_size] + govt_tax
            bill_breakup += f"Topping                                         {topping_price}"
            bill_breakup += f"\n        Total                                           {bill}"
        else:
            bill = pizza_sizes[user_input_pizza_size] + govt_tax
            bill_breakup += f"\n        Total                                           {bill}"
        print(f"Your total today will be ${bill}.\nPrice breakup provided below")
        print(bill_breakup)
else:
    print(f"The pizza size '{user_input_pizza_size}' is not a valid choice. Try again.")