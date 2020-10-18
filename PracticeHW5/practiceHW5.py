from LinkedList import LinkedList
from Validation import Validation
from Iterator import Iterator


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


strategy = 0
first_list = LinkedList()
second_list = LinkedList()
available_linked_lists = []
list_dict = {'1': first_list,
             '2': second_list}
while True:
    menu()
    user_choice = input()
    list_dict = {'1': first_list,
                 '2': second_list}
    if user_choice == 'e':
        break

    elif user_choice == 'i':
        strategy = 1
        print('Strategy 1 chosen')

    elif user_choice == 'f':
        strategy = 2
        print('Strategy 2 chosen')

    elif user_choice == 'g':
        if strategy == 0:
            print('No strategy chosen')
        else:
            print('First list - ', first_list)
            print('Second list - ', second_list)
            chosen = input('Enter the number of the list you want to edit: ')
            if chosen in list_dict:
                list_to_edit = list_dict[chosen]
                position = input('Enter position to insert new values: ')
                if Validation.is_int(position):
                    position = int(position)
                    if Validation.validate_position(position, list_to_edit):
                        to_insert = []
                        done = False
                        if strategy == 1:
                            amount = input('Enter how many Kaprekar numbers you want to generate: ')
                            if Validation.is_int(amount):
                                amount = int(amount)
                                if amount > 0:
                                    iter_obj = Iterator(amount)
                                    for x in iter_obj:
                                        to_insert.append(x)
                                    done = True
                                else:
                                    print('You need to generate something')
                            else:
                                print('Amount of Kaprekar numbers has to be positive')
                        else:
                            file_name = input('Enter the file you want to read from: ')
                            if Validation.validate_file(file_name):
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
                            else:
                                print('Such file does not exist')
                        if done:
                            first_part = LinkedList()
                            for x in to_insert:
                                first_part.append(x)
                            pos = 0
                            for x in list_to_edit:
                                if pos == position:
                                    first_part.get_last().link = x.link
                                    break
                                pos += 1
                            if position == 0:
                                list_to_edit = first_part
                            else:
                                pos = 0
                                for x in list_to_edit:
                                    pos += 1
                                    if pos == position:
                                        x.link = first_part.get_head()
                                        break
                            if chosen == '1':
                                first_list = list_to_edit
                            else:
                                second_list = list_to_edit
                            print('Edited linked list - ', list_to_edit)
                    else:
                        print('Position not valid')
                else:
                    print('Position has to be an integer value')
            else:
                print('We have only list 1 and list 2')

    elif user_choice == 's':
        print('First list - ', first_list)
        print('Second list - ', second_list)

    elif user_choice == 'd':
        print('First list - ', first_list)
        print('Second list - ', second_list)
        chosen = input('Enter the number of the list you want to edit: ')
        if chosen in list_dict:
            list_to_edit = list_dict[chosen]
            position = input('Enter position to delete an element: ')
            if Validation.is_int(position):
                position = int(position)
                if Validation.validate_position(position, list_to_edit) and position != len(list_to_edit):
                    list_to_edit.remove_at(position)
                    print('List with element removed at position', position, list_to_edit)
                    if chosen == '1':
                        first_list = list_to_edit
                    else:
                        second_list = list_to_edit
                else:
                    print('Wrong position value')
            else:
                print('Position has to be an integer')
        else:
            print('No such linked list')

    elif user_choice == 'dd':
        print('First list - ', first_list)
        print('Second list - ', second_list)
        chosen = input('Enter the number of the list you want to edit: ')
        if chosen in list_dict:
            list_to_edit = list_dict[chosen]
            pos_fr = input('Enter position from which to delete elements: ')
            pos_to = input('Enter position to which elements will be deleted: ')
            if Validation.is_int(pos_fr) and Validation.is_int(pos_to):
                pos_fr = int(pos_fr)
                pos_to = int(pos_to)
                if Validation.validate_from_to(pos_fr, pos_to, list_to_edit):
                    list_to_edit.remove_from_to(pos_fr, pos_to)
                    print('List with element removed at positions from', pos_fr, 'to', pos_to, '-', list_to_edit)
                    if chosen == '1':
                        first_list = list_to_edit
                    else:
                        second_list = list_to_edit
                else:
                    print('Invalid positions')
            else:
                print('Positions have to be integers')
        else:
            print('No such linked list')

    elif user_choice == 'm':
        if len(first_list) == len(second_list):
            merged_binary = merge(first_list, second_list)
            print('Binary list -', merged_binary)
            print('Binary list to decimal number -', to_decimal(merged_binary))
        else:
            print('Lists have different size')

    else:
        print('Only choices i, f, g, d, dd, m, s, e are possible')
