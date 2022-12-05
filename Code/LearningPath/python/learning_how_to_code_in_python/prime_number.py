# Find all prime numbers till n

n = 100
for _i in range(2,n):
    for _j in range(2,_i):
        if _i % _j == 0:
            print(f"{_i} is divisible by {_j}")
            break
    else:
        print(f"{_i} is a prime number.")
