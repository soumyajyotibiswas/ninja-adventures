# Print out numbers from 1 to 100 (including 100).
# But, instead of printing multiples of 3, print "Fizz"
# Instead of printing multiples of 5, print "Buzz"
# Instead of printing multiples of both 3 and 5, print "FizzBuzz".

for _i in range(1, 101):
    if _i % 15 == 0:
        print("FizzBuzz")
    elif _i % 3 == 0:
        print("Fizz")
    elif _i % 5 == 0:
        print("Buzz")
    else:
        print(_i)

for _i in range(1, 101):
    _to_print = _i
    if _i % 3 == 0:
        _to_print = "Fizz"
        if _i % 5 == 0:
            _to_print += "Buzz"
    elif _i % 5 == 0:
        _to_print = "Buzz"
    print(_to_print)
