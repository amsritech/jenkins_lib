arr = [7,12,9,4,11,8]
min_val = max_val = arr[0]

for num in arr:
    if num < min_val:
        min_val = num
    if num > max_val:
        max_val = num

print("min num is:", min_val)
print("max num is:", max_val)
