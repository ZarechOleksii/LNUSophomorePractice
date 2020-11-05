class LinkedListIterator:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current:
            to_return = self.current
            self.current = self.current.link
            return to_return
        else:
            raise StopIteration
