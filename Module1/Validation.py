from datetime import date


class Validation:

    @staticmethod
    def salary_decorator(salary_setter):
        def salary_validator(employee, g_salary):
            try:
                g_salary = round(float(g_salary), 2)
            except ValueError:
                print('Salary has to be a positive number')
                return False
            if g_salary < 0:
                print('Salary has to be a positive number')
                return False
            return salary_setter(employee, g_salary)
        return salary_validator

    @staticmethod
    def name_decorator(name_setter):
        def name_validator(employee, g_name):
            if g_name[0].isalpha() and g_name[1].isalpha():
                g_name = g_name[0] + ' ' + g_name[1]
                return name_setter(employee, g_name)
            else:
                print('Name should not contain special characters')
                return False
        return name_validator

    @staticmethod
    def first_date_decorator(date_setter):
        def date_validator(employee, g_date_list):
            try:
                for q in range(0, len(g_date_list)):
                    g_date_list[q] = int(g_date_list[q])
                g_date = date(g_date_list[0], g_date_list[1], g_date_list[2])
                compare_date = date(2015, 8, 5)
                if g_date < compare_date:
                    print('Minimum date is 5th of August 2015')
                    return False
                if g_date > date.today():
                    print('Date cannot be in the future')
                    return False
            except ValueError:
                print('Date values need to be integers of existing date')
                return False
            return date_setter(employee, g_date)
        return date_validator

    @staticmethod
    def last_date_decorator(date_setter):
        def date_validator(employee, g_date_list):
            if g_date_list is None:
                return date_setter(employee, None)
            else:
                try:
                    for q in range(0, len(g_date_list)):
                        g_date_list[q] = int(g_date_list[q])
                    g_date = date(g_date_list[0], g_date_list[1], g_date_list[2])
                    if g_date > date.today():
                        print('Date cannot be in the future')
                        return False
                except ValueError:
                    print('Date values need to be integers of existing date')
                    return False
                return date_setter(employee, g_date)
        return date_validator

    @staticmethod
    def file_name_decorator(employee_init):
        def file_validator(employee_self):
            try:
                file_name = input('Enter file name: ')
                val_file = open(file_name, 'r')
                val_file.close()
                return employee_init(employee_self, file_name)
            except FileNotFoundError:
                return file_validator(employee_self)
        return file_validator
