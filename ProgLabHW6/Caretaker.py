import copy


class Caretaker:
    def __init__(self):
        self.description_history = []
        self.momento_history = []
        self.pointer = -1
        self.undone = 0

    def new_action(self, new_momento, new_desc):
        while self.undone != 0:
            self.momento_history.pop()
            self.description_history.pop()
            self.undone -= 1
        self.description_history.append(new_desc)
        self.momento_history.append(new_momento)
        if self.pointer == 5:
            self.description_history.pop(0)
            self.momento_history.pop(0)
        else:
            self.pointer += 1

    def __str__(self):
        to_return = ''
        for q in range(0, len(self.momento_history)):
            to_return += str(q + 1) + '.' + self.description_history[q] + '\n'
        return to_return

    def undo(self):
        if self.pointer != 0:
            self.pointer -= 1
            self.undone += 1
            print('Undone')
            print('Now on step', str(self.pointer + 1))
            return copy.deepcopy(self.momento_history[self.pointer])
        else:
            print('Cannot undo further')
            print('Now on step', str(self.pointer + 1))
            return False

    def redo(self):
        if self.undone > 0:
            self.pointer += 1
            self.undone -= 1
            print('Redone')
            print('Now on step', str(self.pointer + 1))
            return copy.deepcopy(self.momento_history[self.pointer])
        else:
            print('Cannot redo further')
            print('Now on step', str(self.pointer + 1))
            return False
