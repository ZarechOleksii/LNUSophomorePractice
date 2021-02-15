from Validation import Validation
from Employee import Employee


class AllEmployees:

    list_to_read = ['name', 'salary', 'first_date', 'last_date']

    @Validation.file_name_decorator
    def __init__(self, file_name):
        line = 0
        self.all_employees = []
        self.open_file = file_name
        dict_to_read = dict()
        reading = open(self.open_file, 'r')
        file_list = reading.readlines()
        for x in file_list:
            line += 1
            print('Line', line, 'initialization:')
            line_list = x.split('| ')
            for y in range(0, len(line_list)):
                dict_to_read[self.list_to_read[y]] = line_list[y]
            dict_to_read['name'] = dict_to_read['name'].split()
            dict_to_read['first_date'] = dict_to_read['first_date'].split('-')
            dict_to_read['last_date'] = dict_to_read['last_date'].split('-')
            new_employee = Employee(dict_to_read)
            if new_employee.salary != -1:
                self.all_employees.append(new_employee)
                print('Line', line, 'initialized properly')
            else:
                print('Line', line, 'was not initialized properly')
        reading.close()

    def append(self, new_emp):
        self.all_employees.append(new_emp)

    def __str__(self):
        to_return_all = ''
        for q in range(0, len(self.all_employees)):
            to_return_all += str(self.all_employees[q])
        return to_return_all

    def __len__(self):
        return len(self.all_employees)

    def get_yearly(self):
        to_return_all = ''
        for q in range(0, len(self.all_employees)):
            start_date = self.all_employees[q].first_date.strftime("%d")
            start_date += self.all_employees[q].first_date.strftime("%m")
            finish_date = self.all_employees[q].last_date.strftime("%d")
            finish_date += self.all_employees[q].last_date.strftime("%m")
            if start_date == finish_date:
                to_return_all += str(self.all_employees[q])
        return to_return_all
