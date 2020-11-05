from Node import Node
from LinkedListIterator import LinkedListIterator
from Validation import Validation
from Event import Event
import copy


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

    @Validation.decorator_is_int
    @Validation.decorator_position_delete
    def remove_at(self, position):
        before = copy.deepcopy(self)
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
        Event.to_do('delete', [before, position, self])
        return True

    @Validation.decorator_are_int
    @Validation.decorator_positions_delete
    def remove_from_to(self, posit_from, posit_to):
        before = copy.deepcopy(self)
        to_do = posit_to - posit_from
        if posit_from == 0:
            while to_do != -1:
                self.remove_first()
                to_do -= 1
        elif posit_to == len(self) - 1:
            while to_do != -1:
                self.remove_last()
                to_do -= 1
        else:
            from_delete = self.head
            iteration = 1
            while iteration != posit_from:
                from_delete = from_delete.link
                iteration += 1
            to_delete = from_delete.link
            while to_do != -1:
                to_delete = to_delete.link
                to_do -= 1
            from_delete.link = to_delete
        Event.to_do('delete', [before, [posit_from, posit_to], self])
        return True

    def get_head(self):
        return self.head

    def get_last(self):
        traversal = self.head
        while traversal.link:
            traversal = traversal.link
        return traversal
