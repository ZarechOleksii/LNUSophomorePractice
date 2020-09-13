def game(quantity, numbers):
    sum1 = 0
    sum2 = 0
    odd_indexes_sum = 0
    even_indexes_sum = 0
    if quantity % 2 == 0:
        for i in range(0, quantity):
            if i % 2 == 0:
                even_indexes_sum += numbers[i]
            else:
                odd_indexes_sum += numbers[i]
        if even_indexes_sum > odd_indexes_sum:
            for i in range(0, quantity // 2):
                to_delete = last(numbers)
                if to_delete % 2 == 0:
                    sum1 += numbers[to_delete]
                    numbers[to_delete] = 0
                    to_delete = lowest_diff(numbers)
                    sum2 += numbers[to_delete]
                    numbers[to_delete] = 0
                else:
                    to_delete = first(numbers)
                    sum1 += numbers[to_delete]
                    numbers[to_delete] = 0
                    to_delete = lowest_diff(numbers)
                    sum2 += numbers[to_delete]
                    numbers[to_delete] = 0
        else:
            for i in range(0, quantity // 2):
                to_delete = last(numbers)
                if to_delete % 2 == 1:
                    sum1 += numbers[to_delete]
                    numbers[to_delete] = 0
                    to_delete = lowest_diff(numbers)
                    sum2 += numbers[to_delete]
                    numbers[to_delete] = 0
                else:
                    to_delete = first(numbers)
                    sum1 += numbers[to_delete]
                    numbers[to_delete] = 0
                    to_delete = lowest_diff(numbers)
                    sum2 += numbers[to_delete]
                    numbers[to_delete] = 0
    else:
        to_delete = lowest_diff(numbers)
        sum1 += numbers[to_delete]
        del numbers[to_delete]
        for i in range(0, quantity - 1):
            if i % 2 == 0:
                even_indexes_sum += numbers[i]
            else:
                odd_indexes_sum += numbers[i]
        if even_indexes_sum > odd_indexes_sum:
            for i in range(0, (quantity - 1) // 2):
                to_delete = last(numbers)
                if to_delete % 2 == 0:
                    sum2 += numbers[to_delete]
                    numbers[to_delete] = 0
                    to_delete = lowest_diff(numbers)
                    sum1 += numbers[to_delete]
                    numbers[to_delete] = 0
                else:
                    to_delete = first(numbers)
                    sum2 += numbers[to_delete]
                    numbers[to_delete] = 0
                    to_delete = lowest_diff(numbers)
                    sum1 += numbers[to_delete]
                    numbers[to_delete] = 0
        else:
            for i in range(0, (quantity - 1) // 2):
                to_delete = last(numbers)
                if to_delete % 2 == 1:
                    sum2 += numbers[to_delete]
                    numbers[to_delete] = 0
                    to_delete = lowest_diff(numbers)
                    sum1 += numbers[to_delete]
                    numbers[to_delete] = 0
                else:
                    to_delete = first(numbers)
                    sum2 += numbers[to_delete]
                    numbers[to_delete] = 0
                    to_delete = lowest_diff(numbers)
                    sum1 += numbers[to_delete]
                    numbers[to_delete] = 0
    if sum1 > sum2:
        print('Player ', 1, ' won')
    elif sum2 > sum1:
        print('Player ', 2, ' won')
    else:
        print('Player ', 0, ' won (draw)')
    print('Player 1 - ', sum1)
    print('Player 2 - ', sum2)


def lowest_diff(numbers):
    if numbers[first(numbers)] - numbers[first(numbers) + 1] > numbers[last(numbers)] - numbers[last(numbers) - 1]:
        return first(numbers)
    else:
        return last(numbers)


def first(numbers):
    for x in range(0, len(numbers)):
        if numbers[x] != 0:
            return x


def last(numbers):
    for x in range(len(numbers), -1, - 1):
        if numbers[x - 1] != 0:
            return x - 1


print('Enter the amount of elements you want to play with(up to 100):')
amount = int(input())
elements = [int(x) for x in input("Enter multiple values(up to 1000): ").split()]
no_error = True
for x in range(0, len(elements)):
    if elements[x] > 999:
        no_error = False
if len(elements) == amount and amount < 100 and no_error:
    game(amount, elements)
else:
    print('Wrong input')
