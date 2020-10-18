from Node import Node
from LinkedListIterator import LinkedListIterator


class LinkedList:
    def __init__(self):
        self.head = None
        self.iterator = self.head

    def __len__(self):
        traversal = self.head
        to_return = 0
        while traversal:
            to_return += 1
            traversal = traversal.link
        return to_return

    def __repr__(self):
        to_return = []
        traversal = self.head
        while traversal:
            to_return.append(str(traversal.data))
            traversal = traversal.link
        return '[' + ', '.join(to_return) + ']'

    def append(self, inside):
        new_node = Node(inside)
        if self.head:
            traversal = self.head
            while traversal.link:
                traversal = traversal.link
            traversal.link = new_node
        else:
            self.head = new_node

    def prepend(self, inside):
        new_node = Node(inside)
        new_node.link = self.head
        self.head = new_node

    def __iter__(self):
        return LinkedListIterator(self.head)

    def __next__(self):
        current = self.iterator
        if self.iterator:
            self.iterator = self.iterator.link
        else:
            self.iterator = self.head
            raise StopIteration
        return current

    def remove_last(self):
        if self.head is None:
            print('Nothing to remove')
        else:
            if self.head.link is None:
                self.head = None
            else:
                traversal = self.head
                while traversal.link.link:
                    traversal = traversal.link
                traversal.link = None

    def remove_first(self):
        if self.head is None:
            print('Nothing to remove')
        else:
            the_next = self.head.link
            self.head = None
            self.head = the_next

    def remove_at(self, position):
        if position == 0:
            self.remove_first()
        elif position == len(self) - 1:
            self.remove_last()
        else:
            current = 0
            traversal = self.head
            while position - 1 != current:
                current += 1
                traversal = traversal.link
            traversal.link = traversal.link.link

    def remove_from_to(self, posit_from, posit_to):
        to_do = posit_to - posit_from
        while to_do != -1:
            self.remove_at(posit_from)
            to_do -= 1

    def get_head(self):
        return self.head

    def get_last(self):
        traversal = self.head
        while traversal.link:
            traversal = traversal.link
        return traversal
