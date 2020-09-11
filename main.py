
def task_six(n):
    to_answer = []
    x = 1
    while len(to_answer) != n:
        for y in range(1, len(str((x ** 2))) + 1):
            if (((x ** 2) % (10 ** y)) + ((x ** 2) // (10 ** y)) == x) and ((x ** 2) % (10 ** y) != 0):
                to_answer.append(x)
                break
        x = x + 1
    return to_answer


print('\nEnter the quantity of Kaprekar numbers:')
taskSixN = int(input())
print('First ', taskSixN, ' Kaprekar numbers are: ', task_six(taskSixN))
