def menu():
    print('Enter n to create a new matrix of size n*n')
    print('Enter s to show all matrices')
    print('Enter d to delete a matrix')
    print('Enter e to exit')


def create_matrix(size):
    new_matrix = []
    for x in range(0, size):
        new_matrix.append([])
    mid = size // 2

    for x in range(0, mid):
        adding_values(new_matrix, size, x)
    if (size % 2) == 1:
        adding_values(new_matrix, size, mid)
    for x in range(mid - 1, -1, -1):
        adding_values(new_matrix, size, x)
    return new_matrix


def adding_values(new_matrix_column, row_size, iterator):
    for y in range(0, iterator):
        new_matrix_column[y].append(0)
    for y in range(iterator, row_size - iterator):
        new_matrix_column[y].append(1)
    for y in range(row_size - iterator, row_size):
        new_matrix_column[y].append(0)


def show_all(matrix_list):
    for q in range(0, len(matrix_list)):
        print('\nMatrix', (q + 1))
        for z in range(0, len(matrix_list[q])):
            print(matrix_list[q][z])


all_matrix = []
while True:
    menu()
    user_choice = input()

    if user_choice == 'n':
        try:
            matrix_size = int(input('Enter size of a new matrix: '))
            if matrix_size < 1:
                raise ValueError
            else:
                all_matrix.append(create_matrix(matrix_size))
                print('Matrix with size', matrix_size, 'created')
        except ValueError:
            print('Wrong input, need positive integer')

    elif user_choice == 'e':
        break

    elif user_choice == 's':
        if len(all_matrix) > 0:
            show_all(all_matrix)
        else:
            print('No matrices to display')

    elif user_choice == 'd':
        if len(all_matrix) > 0:
            show_all(all_matrix)
            try:
                matrix_choice = int(input('Enter the number of a matrix you want to delete: '))
                if matrix_choice <= 0:
                    raise ValueError
                all_matrix.pop(matrix_choice - 1)
                print('Successfully removed matrix', matrix_choice)
            except ValueError:
                print('Wrong input, enter positive integer')
            except IndexError:
                print('No such array')
        else:
            print('No matrices to delete')

    else:
        print('Wrong Input, only choices n, s, d and e are available')
