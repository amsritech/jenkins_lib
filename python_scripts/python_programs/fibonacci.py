n = int(input("Enter how many Fibonacci numbers you want: "))
a, b = 0, 1

for _ in range(n):
    print(a, end=", ")
    a, b = b, a + b


###recursion method
def fib(n):
    if n <= 1:
        return n
    return fib(n-1)+fib(n-2)
for i in range(20):
    print(fib(i), end = "")
