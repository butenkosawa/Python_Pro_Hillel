data = [1, 2, 3, 4]


class DeduplicationIterator:
    def __init__(self, data: list[int]) -> None:
        self.data = set(data)

    def __next__(self):
        for i in self.data:
            return i

    def __iter__(self):
        for i in self.data:
            yield i


# for i in data:
#     print(i)

# for i in DeduplicationIterator(data):
#     print(i)

iterator = DeduplicationIterator(data=data)
print(next(iterator))