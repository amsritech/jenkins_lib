def reverse(arr, s, e):
    while s < e:
        arr[s], arr[e] = arr[e], arr[s]
        s += 1
        e -= 1
def rotateleft(arr, d):
    n = len(arr)
    d = d % n 
    reverse(arr, 0 , d-1)
    reverse(arr, d, n-1)
    reverse(arr, 0 , n-1)
    return arr
print(rotateleft([1,2,3,4,5], 2))
###rotate right
#reverse(arr, 0 , n-1)
#reverse(arr, 0 , d-1)
 #reverse(arr, d, n-1)


