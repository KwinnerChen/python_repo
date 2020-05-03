def simple_coro(a):
    print("started a = ", a)
    b = yield a
    print("recieved b = ", b)
    c = yield a + b
    print("recieved c = ", c)
    yield a + b + c


def gener():
    yield from (1,2,3,4)


# class Value:
#     def __init__(self, name, value):
#         self.name = name
#         self.value = value

#     def __str__(self):
#         return f"<{self.name}: {self.name}>"

#     __repr__ = __str__


# class A(type):
#     def __new__(cls, name, bases, attrs):
#         pass


from enum import Enum
from collections import namedtuple

Result = namedtuple('Result', 'count average')

def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total/count
    return Result(count, average)

def grouper(result, key):
    while True:
        result[key] = yield from averager()

def main(data):
    result = {}
    for k, v in data.items():
        group = grouper(result, k)
        next(group)
        for value in v:
            group.send(value)
        group.send(None)
    print(result)


if __name__ == '__main__':
    # coro = simple_coro(1)
    # result = next(coro)
    # print("product result = ", result)
    # result = coro.send(2)
    # print("product result = ", result)
    # result = coro.send(10)
    # print("product result = ", result)
    data = {
        'girls; kg': [40.9, 38.5, 44.3, 42.2, 45.2],
        'girls; m': [1.6, 1.51, 1.4, 1.3]
    }
    main(data)