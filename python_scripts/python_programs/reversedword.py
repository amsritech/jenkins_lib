def reverse_words(s):
    words = s.split()
    left, right = 0, len(words) - 1

    while left < right:
        words[left], words[right] = words[right], words[left]
        left += 1
        right -= 1

    return " ".join(words)

print(reverse_words("my name is srinivas"))