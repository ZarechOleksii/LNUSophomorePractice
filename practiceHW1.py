def game(quantity, numbers):
    sum1, sum2, odd_indexes_sum, even_indexes_sum = 0, 0, 0, 0
    change = False
    if quantity % 2 == 1:
        to_delete = lowest_diff(numbers)
        sum2 += numbers[to_delete]
        del numbers[to_delete]
        change = True
        quantity = quantity - 1

    for i in range(0, quantity):
        if i % 2 == 0:
            even_indexes_sum += numbers[i]
        else:
            odd_indexes_sum += numbers[i]

    if even_indexes_sum > odd_indexes_sum:
        looking_for_remainder = 0
    else:
        looking_for_remainder = 1

    for i in range(0, quantity // 2):
        if last(numbers) % 2 == looking_for_remainder:
            to_delete = last(numbers)
        else:
            to_delete = first(numbers)

        sum1 += numbers[to_delete]
        numbers[to_delete] = 0
        to_delete = lowest_diff(numbers)
        sum2 += numbers[to_delete]
        numbers[to_delete] = 0

    answers = [sum1, sum2]
    if change:
        answers.reverse()
    if answers[0] > answers[1]:
        answers.append(1)
    elif answers[1] > answers[0]:
        answers.append(2)
    else:
        answers.append(0)
    return answers


def lowest_diff(numbers):
    first_value = first(numbers)
    last_value = last(numbers)
    if numbers[first_value] - numbers[first_value + 1] > numbers[last_value] - numbers[last_value - 1]:
        return first_value
    else:
        return last_value


def first(numbers):
    for y in range(0, len(numbers)):
        if numbers[y] != 0:
            return y


def last(numbers):
    for z in range(len(numbers), -1, - 1):
        if numbers[z - 1] != 0:
            return z - 1


try:
    print('Enter the amount of elements you want to play with(up to 100):')
    amount = int(input())
    elements = list(map(int, input('Enter multiple values(up to 1000) separated by space: ').split()))
    for x in range(0, len(elements)):
        if elements[x] > 999 or elements[x] < 1:
            raise ValueError
    if len(elements) != amount or amount > 100 or amount < 1:
        raise ValueError
    else:
        result = game(amount, elements)
        print('Player', result[2], 'won')
        print('Player 1 score =', result[0])
        print('Player 2 score =', result[1])
except ValueError:
    print('Wrong input')

