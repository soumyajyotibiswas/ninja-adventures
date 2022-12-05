"""
Exercise: a simple text menu (Python 3.10)
In this exercise you'll be implementing a simple user menu.

A menu is something that repeats over and over again until the user types something that makes the program terminate.

In our menu, the user will be able to choose from two options:

If they type p , we will print "Hello"

If they type q , we will terminate the program

How will we go about it?

First, we'll ask the user for what they want to do first. Do they want to print (p ), or do they want to exit without printing (q )?

Then we'll have a while  loop that will repeat until the user types q .

Inside the while loop, we'll have an if  statement that checks whether the user typed p . If they did, we'll print "Hello" .

Inside the loop but outside the if statement, we'll ask the user again whether they want to print or quit.

Ask the user to choose one of two options:
if they type 'p', our program should print "Hello" and then ask the user again. Keep repeating this until...
if they type 'q', our program should terminate.


Let's begin by asking the user to type either 'p' or 'q'. You know how to do this using input()
user_input = ...


Then, begin a while loop that runs for as long as the user doesn't type 'q'.
Inside the loop, have an if statement that checks if the user typed 'p'.
   If they did, print "Hello"
Still inside the loop, ask the user again
user_input = ...
"""

user_input = input("Enter your choice: p | q")

while user_input != "q":
    if user_input == "p":
        print("Hello")
    user_input = input("Enter your choice: p | q")
