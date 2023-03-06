intro_message='''
Welcome to the FizzBuzz program.
Enter a number, and the program will print
Fizz if the any number upto your number is divisible
by 3, Buzz if the number is divisible by 5, and FizzBuzz
if the number is divisible by both 3 and 5.
'''
# One liner below:
# ['Fizz'*(not i%3)+'Buzz'*(not i%5) or i for i in range(1,101)]
print(intro_message)
user_number=int(input("Enter your number: "))
for number in range(1,(user_number+1)):
    to_print=""
    if number % 3 == 0:
        to_print='Fizz'
        if number % 5 == 0:
            to_print+='Buzz'
    elif number % 5 == 0:
        to_print='Buzz'
    else:
        to_print=number
    print(to_print)