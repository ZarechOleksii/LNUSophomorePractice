from AllEmployees import AllEmployees
from Employee import Employee


def menu():
    print('\nA to add')
    print('P to show all')
    print('W to write yearly employees in file')
    print('Q to quit\n')


all_employees = AllEmployees()

while True:
    menu()
    action = input()
    if action == 'Q':
        break
    elif action == 'A':
        initial_dict = dict()
        initial_dict['name'] = input('Enter name of the employee separated by space: ').split()
        initial_dict['salary'] = input('Enter salary of the employee: ')
        new_year = input('Enter the year of starting: ')
        new_month = input('Enter the month of starting: ')
        new_day = input('Enter the day of the starting: ')
        initial_dict['first_date'] = [new_year, new_month, new_day]
        print('Is he retired(Y/N)?')
        user_input = input()
        if user_input == 'N':
            initial_dict['last_date'] = None
        else:
            new_year = input('Enter the year of finishing: ')
            new_month = input('Enter the month of finishing: ')
            new_day = input('Enter the day of the finishing: ')
            initial_dict['last_date'] = [new_year, new_month, new_day]
        new_employee = Employee(initial_dict)
        if new_employee.salary != -1:
            all_employees.append(new_employee)
            print(new_employee)
            print('New object successfully created')
        else:
            print('New object was not created')

    elif action == 'P':
        print(all_employees)
    elif action == 'W':
        new_file = input('Enter file name to write: ')
        writing = open(new_file, 'w')
        writing.write(all_employees.get_yearly())
        writing.close()
    else:
        print('No such option')
