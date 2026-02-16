n = 5
fact = 1

for i in range(1, n + 1):
    fact *= i

print(fact)


##############recursion########################################

def factorial(n):
    if n ==0 or n ==1:
        return 1
    return n * factorial(n-1)
print(factorial(5))