
def find_kaprekar(amount):
    to_answer = []
    x = 1
    while len(to_answer) != amount:
        for y in range(1, len(str((x ** 2))) + 1):
            if (((x ** 2) % (10 ** y)) + ((x ** 2) // (10 ** y)) == x) and ((x ** 2) % (10 ** y) != 0):
                to_answer.append(x)
                break
        x = x + 1
    return to_answer


try:
    print('\nEnter the quantity of Kaprekar numbers:')
    quantity = int(input())
    if quantity < 0:
        raise ValueError
    print('First ', quantity, ' Kaprekar numbers are: ', find_kaprekar(quantity))
except ValueError:
    print('Wrong input, enter a positive integer')
