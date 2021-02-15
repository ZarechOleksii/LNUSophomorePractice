
def generator():
    x = 1
    while True:
        for y in range(1, len(str((x ** 2))) + 1):
            if (((x ** 2) % (10 ** y)) + ((x ** 2) // (10 ** y)) == x) and ((x ** 2) % (10 ** y) != 0):
                yield x
        x += 1
