import random
from LinkedList import LinkedList


def to_decimal(binary):
    decimal = 0
    for z in range(0, len(binary)):
        decimal = decimal * 2
        decimal = decimal + binary.iterate()
    return decimal


def merge(to_merge_first, to_merge_second):
    merged = LinkedList()
    for z in range(0, len(to_merge_first)):
        if to_merge_first.iterate() > to_merge_second.iterate():
            merged.append(1)
        else:
            merged.append(0)
    return merged


def menu():
    print('\nChoose your action:\n1.Enter a to create a new linked list with size N and random numbers')
    print('2.Enter b to create a new custom linked list\n3.Enter s to see present lists')
    print('4.Enter d to delete a list')
    print('5.Enter m to merge two lists into a binary list and transform it to a decimal number')
    print('6.Enter e to exit menu')


def random_list(size, lower_bound, higher_bound):
    new_linked_list = LinkedList()
    for z in range(0, size):
        new_linked_list.prepend(random.randint(lower_bound, higher_bound))
    return new_linked_list


tester = LinkedList()
available_linked_lists = []
while True:
    menu()
    user_choice = input()

    if user_choice == 'e':
        break

    elif user_choice == 'a':
        try:
            new_list_size = int(input('Enter the size of a new linked list: '))
            lower_end = int(input('Enter the lower end of possible random numbers: '))
            higher_end = int(input('Enter the higher end of possible random numbers: '))
            if lower_end > higher_end or new_list_size < 0:
                raise ValueError
            available_linked_lists.append(random_list(new_list_size, lower_end, higher_end))
        except ValueError:
            print('Wrong input')

    elif user_choice == 'b':
        try:
            new_size = int(input('Enter the size of a linked list: '))
            if new_size < 0:
                raise ValueError
            new_list = LinkedList()
            for q in range(0, new_size):
                new_list.append(int(input('Enter new element ' + str(q + 1) + ': ')))
            available_linked_lists.append(new_list)
        except ValueError:
            print('Wrong input')

    elif user_choice == 's':
        if len(available_linked_lists) != 0:
            for x in range(0, len(available_linked_lists)):
                print(x + 1, '-', available_linked_lists[x])
        else:
            print('No lists no display')

    elif user_choice == 'd':
        if len(available_linked_lists) > 0:
            try:
                for y in range(0, len(available_linked_lists)):
                    print(y + 1, '-', available_linked_lists[y])
                to_delete = int(input('Enter the number of a list you want to delete: '))
                available_linked_lists.pop(to_delete - 1)
                print('List', to_delete, 'deleted')
            except ValueError:
                print('Need the number of a list')
            except IndexError:
                print('No such list')
        else:
            print('No lists to delete')

    elif user_choice == 'm':
        if len(available_linked_lists) > 1:
            try:
                for y in range(0, len(available_linked_lists)):
                    print(y + 1, '-', available_linked_lists[y])
                first = int(input('Enter the number of the first list to merge: '))
                second = int(input('Enter the number of the second list to merge: '))
                if len(available_linked_lists[first - 1]) == len(available_linked_lists[second - 1]):
                    merged_binary = merge(available_linked_lists[first - 1], available_linked_lists[second - 1])
                    print('Binary list -', merged_binary)
                    print('Binary list to decimal number -', to_decimal(merged_binary))
                else:
                    print('Selected lists have different size')
            except ValueError:
                print('Need the number of a list')
            except IndexError:
                print('No such list')
        else:
            print('Not enough present lists')

    else:
        print('Only choices a, b, d, m, s, e are possible')
