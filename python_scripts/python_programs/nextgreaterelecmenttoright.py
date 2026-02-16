arr = [4, 5, 2, 10, 8]
stack = []
result = [-1] * len(arr)

for i in range(len(arr) - 1, -1, -1):   # scan from right to left
    
    while stack and stack[-1] <= arr[i]:
        stack.pop()
    
    if stack:
        result[i] = stack[-1]
    
    stack.append(arr[i])

print(result)