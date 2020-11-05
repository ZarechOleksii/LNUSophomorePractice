from Strategy import *
from Context import Context
from LinkedList import LinkedList
from Observer import Observer
from Logger import Logger


def to_decimal(binary):
    decimal = 0
    for z in binary:
        decimal = decimal * 2
        decimal = decimal + z.data
    return decimal


def merge(to_merge_first, to_merge_second):
    merged = LinkedList()
    for z, c in zip(to_merge_first, to_merge_second):
        if z.data > c.data:
            merged.append(1)
        else:
            merged.append(0)
    return merged


def menu():
    print('\nChoose your action:')
    print('1.Enter i to choose number generating strategy')
    print('2.Enter f to choose file reading strategy')
    print('3.Enter g to generate data using chosen strategy')
    print('4.Enter d to delete one element in the list')
    print('5.Enter dd to delete multiple elements in the list')
    print('6.Enter m to merge two lists into a binary list and transform it to a decimal number')
    print('7.Enter s to see present lists')
    print('8.Enter e to exit menu')


def print_dict(g_dict):
    print('First list:', g_dict['1'])
    print('Second list:', g_dict['2'])


strategy = 0
first_list = LinkedList()
second_list = LinkedList()
list_dict = {'1': first_list,
             '2': second_list}
context = Context()
first_strategy = FirstStrategy()
second_strategy = SecondStrategy()
Observer.attach('add', Logger.adding_to_list_print)
Observer.attach('delete', Logger.deleting_from_list_print)
Observer.attach('main_func', Logger.main_list_method_print)

while True:
    menu()
    user_choice = input()

    if user_choice == 'e':
        break

    elif user_choice == 'i':
        context.set_strategy(first_strategy)
        print('Strategy 1 chosen')

    elif user_choice == 'f':
        context.set_strategy(second_strategy)
        print('Strategy 2 chosen')

    elif user_choice == 'g':
        print_dict(list_dict)
        chosen = input('Enter the number of the list you want to edit: ')
        if chosen in list_dict:
            position = input('Enter position to insert new values: ')
            param = input('Enter the value of the parameter: ')
            new_list = context.generate(list_dict[chosen], position, param)
            if new_list is not False:
                print('New list:', new_list)
                list_dict[chosen] = new_list
        else:
            print('We have only list 1 and list 2')

    elif user_choice == 's':
        print_dict(list_dict)

    elif user_choice == 'd':
        print_dict(list_dict)
        chosen = input('Enter the number of the list you want to edit: ')
        if chosen in list_dict:
            position = input('Enter position to delete an element: ')
            if list_dict[chosen].remove_at(position):
                print('List with element removed at position', position, list_dict[chosen])
        else:
            print('No such linked list')

    elif user_choice == 'dd':
        print_dict(list_dict)
        chosen = input('Enter the number of the list you want to edit: ')
        if chosen in list_dict:
            pos_fr = input('Enter position from which to delete elements: ')
            pos_to = input('Enter position to which elements will be deleted: ')
            if list_dict[chosen].remove_from_to(pos_fr, pos_to):
                print('List with elements removed from', pos_fr, 'to', pos_to, list_dict[chosen])
        else:
            print('No such linked list')

    elif user_choice == 'm':
        if len(list_dict['1']) == len(list_dict['2']):
            merged_binary = merge(list_dict['1'], list_dict['2'])
            decimal_num = to_decimal(merged_binary)
            print('Binary list -', merged_binary)
            print('Binary list to decimal number -', decimal_num)
            Event.to_do('main_func', [list_dict['1'], list_dict['2'], merged_binary, decimal_num])
        else:
            print('Lists have different size')

    else:
        print('Only choices i, f, g, d, dd, m, s, e are possible')
