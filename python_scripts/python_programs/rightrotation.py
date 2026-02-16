def reverse(arr, s, e):
    while s < e:
        arr[s], arr[e] = arr[e], arr[s]
        s += 1
        e -= 1

def rotate_right(arr, d):
    n = len(arr)
    d = d % n

    reverse(arr, 0, n-1)      # Step 1 reverse whole arry
    reverse(arr, 0, d-1)      # Step 2 reverse fist d elements
    reverse(arr, d, n-1)      # Step 3 reverse remaining

    return arr

print(rotate_right([1,2,3,4,5], 2))


###slicing methd

def rotate_right(arr, d):
    n = len(arr)
    d = d % n
    return arr[-d:] + arr[:-d]

print(rotate_right([1,2,3,4,5], 2))