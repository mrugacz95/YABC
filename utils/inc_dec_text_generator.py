s = "Hello world!\n"  # input()
numbers = [ord(c) for c in s]
result = ""
state = 0
for number in numbers:
    while state != number:
        if state < number:
            result += "+"
            state += 1
        else:
            result += "-"
            state -= 1
    result += "."
line_len = 79
chunks = [result[i:i + line_len] for i in range(0, len(result), line_len)]
print("\n".join(chunks))
