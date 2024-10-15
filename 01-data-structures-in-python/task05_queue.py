print('queue implementation using list')
queue = []

queue.append('a')
queue.append('b')
queue.append('c')

print('Initial queue:')
print(queue)

print('Elements popped from stack:')
print(queue.pop(0))
print(queue.pop(0))

print('Next version of queue:')
print(queue)

queue.append('d')
queue.append('e')

print('Next version of queue:')
print(queue)

print('Element popped from queue:')
print(queue.pop(0))

queue.append('f')

print('Final version of queue:')
print(queue)

print('--------------------------------')

from collections import deque

print('stack implementation using collections.deque')
queue2 = deque()

queue2.append('a')
queue2.append('b')
queue2.append('c')

print('Initial queue:')
print(queue2)

print('Elements popped from queue:')
print(queue2.popleft())
print(queue2.popleft())

print('Next version of queue:')
print(queue2)

queue2.append('d')
queue2.append('e')

print('Next version of queue:')
print(queue2)

print('Element popped from queue:')
print(queue2.popleft())

queue2.append('f')

print('Final version of queue:')
print(queue2)