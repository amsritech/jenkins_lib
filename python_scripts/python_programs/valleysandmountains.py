def counting_valleys(steps, path):
    level = 0
    valleys = 0

    for step in path:
        if step == "U":
            level += 1
            if level == 0:
                valleys += 1   # just came up from a valley
        else:
            level -= 1

    return valleys


steps = 8
path = "UDDDUDUU"

print(counting_valleys(steps, path))
