from Validation import Validation


class Employee:
    setters = {'name': 'set_name',
               'salary': 'set_salary',
               'first_date': 'set_first_date',
               'last_date': 'set_last_date'}

    to_return_dict = {'Name: ': 'name',
                      'Salary: ': 'salary',
                      'Starting date: ': 'first_date',
                      'Last date: ': 'last_date'}

    def __init__(self, init_dict):
        created = True
        for q in self.setters:
            if not getattr(self, self.setters[q])(init_dict[q]):
                created = False
        if not created:
            self.salary = -1

    @Validation.name_decorator
    def set_name(self, g_name):
        self.name = g_name
        return True

    @Validation.salary_decorator
    def set_salary(self, g_salary):
        self.salary = g_salary
        return True

    @Validation.first_date_decorator
    def set_first_date(self, g_date):
        self.first_date = g_date
        return True

    @Validation.last_date_decorator
    def set_last_date(self, g_date):
        if g_date < self.first_date:
            print('Start date later than finish error')
            return False
        else:
            self.last_date = g_date
            return True

    def __str__(self):
        to_return = ''
        for q in self.to_return_dict:
            to_return += q + str(getattr(self, self.to_return_dict[q])) + '\n'
        return to_return
