from IteratorClass import Iterator
from Generator import generator


def menu():
    print('\nA - Find Kaprekar numbers using iterator')
    print('B - Find Kaprekar numbers using generator')
    print('Q - Quit')


while True:
    try:
        menu()
        user_choice = input()
        if user_choice == 'Q':
            break

        if user_choice == 'A' or user_choice == 'B':
            print('\nEnter the quantity of Kaprekar numbers:')
            quantity = int(input())

            if quantity < 0:
                raise ValueError

            answer = []
            if user_choice == 'A':
                print('Looking for first', quantity, 'Kaprekar numbers using Iterator class')
                iter_object = Iterator(quantity)
                for q in iter_object:
                    answer.append(q)

            elif user_choice == 'B':
                print('Looking for first', quantity, 'Kaprekar numbers using generator')
                for q in generator():
                    answer.append(q)
                    if len(answer) == quantity:
                        break

            print('First ', quantity, ' Kaprekar numbers are: ', answer)

        else:
            print('No such option in menu')

    except ValueError:
        print('Wrong input, enter a positive integer')
