class Iterator:
    def __init__(self, n):
        self.x = 0
        self.amount = n
        self.returned = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.returned == self.amount:
            raise StopIteration
        self.returned += 1
        while True:
            self.x += 1
            for y in range(1, len(str((self.x ** 2))) + 1):
                parts = 10 ** y
                if (((self.x ** 2) % parts) + ((self.x ** 2) // parts) == self.x) and ((self.x ** 2) % parts != 0):
                    return self.x
