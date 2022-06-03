"""
Read more about the input function here - https://www.askpython.com/python/built-in-methods/python-input-function
"""

# Does not provide an output to console
input("Hey what is your name?")

# Store input into a variable
x = input("Hey what is your name?")
print(x)

# You can use the input function inside a print function
print("Your name is " + input("Hey! What is your name: "))

# Printing number of characters in a name
print("The number of characters in your name is " + str(len(input("Hey! What is your name: "))))