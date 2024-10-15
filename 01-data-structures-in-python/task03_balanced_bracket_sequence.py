stack = []

def is_correct_sequence(sequence):
    for char in sequence:
        if char == "(" or char == "[" or char == "{":
            stack.append(char)

        if char == ")":
            if len(stack) == 0 or stack.pop() != '(':
                return False
        elif char == "]":
            if len(stack) == 0 or stack.pop() != '[':
                return False
        elif char == "}":
            if len(stack) == 0 or stack.pop() != '{':
                return False

    return len(stack) == 0

sequence = input("Enter string: ")
print(is_correct_sequence(sequence))