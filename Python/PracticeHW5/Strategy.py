import abc
from Validation import Validation
from Iterator import Iterator
from LinkedList import LinkedList


class Strategy:
    @staticmethod
    @abc.abstractmethod
    def generate(l_list, pos, insertion):
        first_part = LinkedList()
        given_list = l_list
        for x in insertion:
            first_part.append(x)
        iterator = 0
        for x in given_list:
            if pos == iterator:
                first_part.get_last().link = x.link
                break
            iterator += 1
        if pos == 0:
            return first_part
        else:
            iterator = 0
            for x in given_list:
                iterator += 1
                if pos == iterator:
                    x.link = first_part.get_head()
                    break
        return given_list


class FirstStrategy(Strategy):
    @Validation.decorator_amount
    def generate(self, l_list, pos, amount):
        to_insert = []
        iter_obj = Iterator(amount)
        for x in iter_obj:
            to_insert.append(x)
        return super().generate(l_list, pos, to_insert)


class SecondStrategy(Strategy):
    @Validation.decorator_file
    def generate(self, l_list, pos, file_name):
        to_insert = open(file_name)
        to_insert = to_insert.read()
        to_insert = to_insert.split('| ')
        done = True
        for x in range(0, len(to_insert)):
            if Validation.is_int(to_insert[x]):
                to_insert[x] = int(to_insert[x])
            else:
                done = False
        if done is False:
            print('Wrong file content, need to be integers separated by "| "')
            return False
        else:
            return super().generate(l_list, pos, to_insert)
