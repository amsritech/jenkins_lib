n =7
ar = [1,2,1,2,1,3,2]
def sockmerchant(n, ar):
    pairs = 0
    set_ar = set(ar)
    for color in set_ar:
        count = ar.count(color)
        pairs += count // 2
    return pairs
print("total paris:", sockmerchant(n, ar))