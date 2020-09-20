import random


def merge(first, second):
    merged = []
    for z in range(0, len(first)):
        if first[z] > second[z]:
            merged.append(1)
        else:
            merged.append(0)
    return merged


def to_decimal(binary):
    decimal = 0
    for z in range(0, len(binary)):
        decimal = decimal * 2
        decimal = decimal + binary[z]
    return decimal


def random_array(new_size_rand, lower_bound, higher_bound):
    new_array_rand = []
    for z in range(0, new_size_rand):
        new_array_rand.append(random.randint(lower_bound, higher_bound))
    return new_array_rand


def menu():
    print('\nChoose your action:\n1.Enter a to create a new array with size N and random numbers')
    print('2.Enter b to create a new custom array\n3.Enter s to see present arrays')
    print('4.Enter d to delete an array\n5.Enter f to sort and find value in an array')
    print('6.Enter m to merge two arrays into a binary array and transform to decimal number')
    print('7.Enter e to exit menu')


available_arrays = []
while True:
    menu()
    user_choice = input()
    if user_choice == 'e':
        break

    elif user_choice == 'a':
        try:
            new_arr_size = int(input('Enter the size of a new array: '))
            lower_end = int(input('Enter the lower end of possible random numbers: '))
            higher_end = int(input('Enter the higher end of possible random numbers: '))
            if lower_end > higher_end or new_arr_size < 0:
                raise ValueError
            available_arrays.append(random_array(new_arr_size, lower_end, higher_end))
        except ValueError:
            print('Wrong input')

    elif user_choice == 'b':
        try:
            new_size = int(input('Enter the size of a new array: '))
            if new_size < 0:
                raise ValueError
            new_array = []
            for q in range(0, new_size):
                new_array.append(int(input('Enter new element ' + str(q + 1) + ': ')))
            available_arrays.append(new_array)
        except ValueError:
            print('Wrong input')

    elif user_choice == 's':
        for x in range(0, len(available_arrays)):
            print(x + 1, '-', available_arrays[x])

    elif user_choice == 'd':
        if len(available_arrays) > 0:
            try:
                for y in range(0, len(available_arrays)):
                    print(y + 1, '-', available_arrays[y])
                to_delete = int(input('Enter the number of an array you want to delete: '))
                available_arrays.pop(to_delete - 1)
            except ValueError:
                print('Need the number of an array')
            except IndexError:
                print('No such array')
        else:
            print('No arrays to delete')

    elif user_choice == 'm':
        if len(available_arrays) > 1:
            try:
                for y in range(0, len(available_arrays)):
                    print(y + 1, '-', available_arrays[y])
                to_merge_first = int(input('Enter the number of the first array to merge: '))
                to_merge_second = int(input('Enter the number of the second array to merge: '))
                if len(available_arrays[to_merge_first - 1]) == len(available_arrays[to_merge_second - 1]):
                    merged_binary = merge(available_arrays[to_merge_first - 1], available_arrays[to_merge_second - 1])
                    print('Binary array -', merged_binary)
                    print('Binary array to decimal number -', to_decimal(merged_binary))
                else:
                    print('Selected arrays have different size')
            except ValueError:
                print('Need the number of an array')
            except IndexError:
                print('No such array')
        else:
            print('Not enough present arrays')

    elif user_choice == 'f':
        if len(available_arrays) > 0:
            for y in range(0, len(available_arrays)):
                print(y + 1, '-', available_arrays[y])
            try:
                actions = 0
                indexes = []
                to_look_inside = available_arrays[int(input('Enter the number of the array to search in: ')) - 1]
                look_for = int(input('Enter a value to find in the array: '))
                print('Looking for', look_for, 'in', to_look_inside, 'using binary search')
                to_look_inside.sort()
                actions += 1
                print(str(actions) + '.Sorted array:', to_look_inside)
                from_pos = 0
                to_pos = len(to_look_inside) - 1
                while to_pos >= from_pos:
                    mid_index = (from_pos + to_pos) // 2
                    actions += 1
                    print(str(actions) + '.Checking at middle index', mid_index)
                    if to_look_inside[mid_index] < look_for:
                        from_pos = mid_index + 1
                        actions += 1
                        print(str(actions) + '.The number we are looking for is in the right half')
                    elif to_look_inside[mid_index] > look_for:
                        to_pos = mid_index - 1
                        actions += 1
                        print(str(actions) + '.The number we are looking for is in the left half')
                    elif to_look_inside[mid_index] == look_for:
                        indexes.append(mid_index)
                        actions += 1
                        print(str(actions) + '.Found first instance of', look_for, 'at index', mid_index)
                        break
                if len(indexes) == 0:
                    print('The number', look_for, 'is not present in array', to_look_inside)
                    print('Actions done =', actions)
                else:
                    for x in range(indexes[0] + 1, len(to_look_inside)):
                        actions += 1
                        print(str(actions) + '.Looking for another instance at index', x)
                        if to_look_inside[x] == look_for:
                            indexes.append(x)
                            actions += 1
                            print(str(actions) + '.Found another instance at index', x)
                        else:
                            actions += 1
                            print(str(actions) + '.Not found at', x)
                            break
                    for x in range(indexes[0] - 1, -1, -1):
                        actions += 1
                        print(str(actions) + '.Looking for another instance at index', x)
                        if to_look_inside[x] == look_for:
                            indexes.append(x)
                            actions += 1
                            print(str(actions) + '.Found another instance at', x)
                        else:
                            actions += 1
                            print(str(actions) + '.Not found at', x)
                            break
                    print('The indexes of number', look_for, 'in array', to_look_inside, 'are', indexes)
                    print('Actions done =', actions)
            except ValueError:
                print('Number needed')
            except IndexError:
                print('No such array')
        else:
            print('Not enough present arrays')
    else:
        print('Only choices a, b, d, m, s, f, e are possible')
