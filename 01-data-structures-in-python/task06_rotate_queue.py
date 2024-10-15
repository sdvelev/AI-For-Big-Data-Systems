class Queue:

    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def __repr__(self):
        return repr(self.items)

def queue_length(queue):
    length = 0
    auxiliary = Queue()

    while not queue.isEmpty():
        length += 1
        auxiliary.enqueue(queue.dequeue())

    while not auxiliary.isEmpty():
        queue.enqueue(auxiliary.dequeue())

    return length

def rotate(queue, n):
    for _ in range(n):
        queue.enqueue(queue.dequeue())

def swap(queue, m, n):
    length = queue_length(queue)

    # Make sure m ≤ n
    if m > n:
        m, n = n, m

    # Rotate to n
    rotate(queue, length-n-1)

    # Pop into temporary storage
    temp = queue.dequeue()

    # Rotate to m
    rotate(queue, n-m-1)

    # Swap
    queue.enqueue(temp)
    temp = queue.dequeue()

    # Rotate to where n was
    rotate(queue, m-n-1+length)

    # Push back
    queue.enqueue(temp)

    # Rotate to start
    rotate(queue, n)

def reverse(queue):
    left = 0
    right = queue_length(queue)-1

    while left < right:
        swap(queue, left, right)
        left += 1
        right -= 1

queue = Queue()
for i in reversed(range(20)):
    queue.enqueue(i)

print(queue)

reverse(queue)
print(queue)