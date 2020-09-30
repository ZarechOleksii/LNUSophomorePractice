from Node import Node


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
            self.reset()

    def prepend(self, inside):
        new_node = Node(inside)
        new_node.link = self.head
        self.head = new_node
        self.reset()

    def iterate(self):
        current = self.iterator
        if self.iterator.link:
            self.iterator = self.iterator.link
        else:
            self.reset()
        return current.data

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
            self.reset()

    def remove_first(self):
        if self.head is None:
            print('Nothing to remove')
        else:
            the_next = self.head.link
            self.head = None
            self.head = the_next
            self.reset()

    def reset(self):
        self.iterator = self.head
