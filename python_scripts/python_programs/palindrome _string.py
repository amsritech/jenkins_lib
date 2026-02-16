
#palindrome string
word = "madam"
if word == word[::-1]:
    print("string is  palindrom")
else:
    print("not a palindrom")
    ##Interview Alternative (Without Slicing) reversed
word = "srinivas"
rev = ""
for ch in word:
  rev = ch + rev
print(rev)

#reversed method
s = 'hello'
rev = ''.join(reversed(s))
print(rev)
######logic method "palindrom numbers printing"

for num in range(1, 200):
    original = num
    rev = 0

    while num > 0:
        digit = num % 10
        rev = rev * 10 + digit
        num //= 10

    if original == rev:
        print(original)



 

