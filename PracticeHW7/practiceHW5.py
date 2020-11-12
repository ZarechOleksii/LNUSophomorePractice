from Strategy import *
from Context import Context
from LinkedList import LinkedList
from Observer import Observer
from Logger import Logger
import threading


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
    decimal = to_decimal(merged)
    Event.to_do('main_func', [to_merge_first, to_merge_second, merged, decimal])
    to_print = 'Binary list - ' + str(merged) + '\n'
    to_print += 'Binary list to decimal number - ' + str(decimal)
    print(to_print)


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


def print_list(l_num, g_list):
    to_print = 'List ' + str(l_num) + ': ' + str(g_list)
    print(to_print)


def print_dict(g_dict):
    threads = []
    for z in list_dict:
        threads.append(threading.Thread(target=print_list, args=(z, g_dict[z],)))
    for z in threads:
        z.start()
    for z in threads:
        z.join()


strategy = 0
first_list = LinkedList()
second_list = LinkedList()
list_dict = {'1': first_list,
             '2': second_list}
context = Context()
first_strategy = FirstStrategy()
second_strategy = SecondStrategy()
Observer.attach('add', Logger.changing_list_print)
Observer.attach('delete', Logger.changing_list_print)
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
        position = input('Enter position to delete an element: ')
        thread1 = threading.Thread(target=list_dict['1'].remove_at, args=(position,))
        thread2 = threading.Thread(target=list_dict['2'].remove_at, args=(position,))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        print('Lists now:')
        print_dict(list_dict)

    elif user_choice == 'dd':
        print_dict(list_dict)
        pos_fr = input('Enter position from which to delete elements: ')
        pos_to = input('Enter position to which elements will be deleted: ')
        thread1 = threading.Thread(target=list_dict['1'].remove_from_to, args=(pos_fr, pos_to,))
        thread2 = threading.Thread(target=list_dict['2'].remove_from_to, args=(pos_fr, pos_to,))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        print('Lists now:')
        print_dict(list_dict)

    elif user_choice == 'm':
        if len(list_dict['1']) == len(list_dict['2']):
            thread1 = threading.Thread(target=merge, args=(list_dict['1'], list_dict['2'],))
            thread2 = threading.Thread(target=merge, args=(list_dict['2'], list_dict['1'],))
            thread1.start()
            thread2.start()
            thread1.join()
            thread2.join()
        else:
            print('Lists have different size')

    else:
        print('Only choices i, f, g, d, dd, m, s, e are possible')
