arr = [-2, -1, -3, 4, -1, 2, 1, -5, 4]

current_sum = arr[0]
max_sum = arr[0]

for num in arr[1:]:
    current_sum = max(num, current_sum + num)
    max_sum = max(max_sum, current_sum)

print("Max subarray sum:", max_sum)