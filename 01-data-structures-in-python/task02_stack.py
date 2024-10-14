print('stack implementation using list')
stack = []

stack.append('a')
stack.append('b')
stack.append('c')

print('Initial stack:')
print(stack)

print('Elements popped from stack:')
print(stack.pop())
print(stack.pop())

print('Next version of stack:')
print(stack)

stack.append('d')
stack.append('e')

print('Next version of stack:')
print(stack)

print('Element popped from stack:')
print(stack.pop())

stack.append('f')

print('Final version of stack:')
print(stack)

print('--------------------------------')

from collections import deque

print('stack implementation using collections.deque')
stack2 = deque()

stack2.append('a')
stack2.append('b')
stack2.append('c')

print('Initial stack:')
print(stack2)

print('Elements popped from stack:')
print(stack2.pop())
print(stack2.pop())

print('Next version of stack:')
print(stack2)

stack2.append('d')
stack2.append('e')

print('Next version of stack:')
print(stack2)

print('Element popped from stack:')
print(stack2.pop())

stack2.append('f')

print('Final version of stack:')
print(stack2)

print('--------------------------------')

print('stack implementation using a linked list node class')

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class Stack:

    # Initializing a stack.
    # Use a dummy node, which is
    # easier for handling edge cases.
    def __init__(self):
        self.head = Node("head")
        self.size = 0

    # String representation of the stack
    def __str__(self):
        cur = self.head.next
        out = ""
        while cur:
            out += str(cur.value) + "->"
            cur = cur.next
        return out[:-2]

    # Get the current size of the stack
    def getSize(self):
        return self.size

    # Check if the stack is empty
    def isEmpty(self):
        return self.size == 0

    # Get the top item of the stack
    def peek(self):

        # Sanitary check to see if we
        # are peeking an empty stack.
        if self.isEmpty():
            raise Exception("Peeking from an empty stack")
        return self.head.next.value

    # Push a value into the stack.
    def push(self, value):
        node = Node(value)
        node.next = self.head.next
        self.head.next = node
        self.size += 1

    # Remove a value from the stack and return.
    def pop(self):
        if self.isEmpty():
            raise Exception("Popping from an empty stack")
        remove = self.head.next
        self.head.next = self.head.next.next
        self.size -= 1
        return remove.value


# Driver Code
if __name__ == "__main__":
    stack = Stack()
    for i in range(1, 11):
        stack.push(i)
    print(f"Stack: {stack}")

    for _ in range(1, 6):
        remove = stack.pop()
        print(f"Pop: {remove}")
    print(f"Stack: {stack}")