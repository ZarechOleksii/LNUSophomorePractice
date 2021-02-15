import datetime
from RestaurantNames import RestaurantName


class Validation:

    @staticmethod
    def validate_int(given):
        try:
            int(given)
            return False
        except ValueError:
            return True

    @staticmethod
    def file_name_decorator_validate(col_init):
        def file_validator(col_self, g_file_name):
            try:
                val_file = open(g_file_name, 'r')
                val_file.close()
                return col_init(col_self, g_file_name)
            except FileNotFoundError:
                g_file_name = input('Enter file name: ')
                return file_validator(col_self, g_file_name)
        return file_validator

    @staticmethod
    def id_decorator_validate(id_setter):
        def id_validator(event_self, g_id):
            try:
                g_id = int(g_id)
            except ValueError:
                print('ID has to be a positive integer')
                return False
            if g_id < 1:
                print('ID has to be a positive integer')
                return False
            return id_setter(event_self, g_id)
        return id_validator

    @staticmethod
    def title_decorator_validate(title_setter):
        def title_validator(event_self, g_title):
            for q in g_title:
                if q == '|' or q == '-' or q == ':':
                    print('Title should not contain symbols "-", "|" and ":"')
                    return False
            return title_setter(event_self, g_title)
        return title_validator

    @staticmethod
    def rest_decorator_validate(rest_setter):
        def rest_validator(event_self, g_rest):
            try:
                g_rest = RestaurantName(int(g_rest))
            except ValueError:
                print('Restaurant should be a number of the restaurant from the list')
                return False
            return rest_setter(event_self, g_rest)
        return rest_validator

    @staticmethod
    def date_decorator_validate(date_setter):
        def date_validator(event_self, g_date_list):
            try:
                for q in range(0, len(g_date_list)):
                    g_date_list[q] = int(g_date_list[q])
                g_date = datetime.date(g_date_list[0], g_date_list[1], g_date_list[2])
            except ValueError:
                print('Date values need to be integers of existing date')
                return False
            except IndexError:
                print('Wrong date input format')
                return False
            return date_setter(event_self, g_date)
        return date_validator

    @staticmethod
    def time_decorator_validate(time_setter):
        def time_validator(event_self, g_time_list):
            try:
                for q in range(0, len(g_time_list)):
                    g_time_list[q] = int(g_time_list[q])
                g_time = datetime.time(g_time_list[0], g_time_list[1])
            except ValueError:
                print('Time values need to be integers from 0 to 23 for hours and from 0 to 59 for minutes')
                return False
            except IndexError:
                print('Wrong time input format')
                return False
            return time_setter(event_self, g_time)
        return time_validator

    @staticmethod
    def duration_decorator_validate(duration_setter):
        def duration_validator(event_self, g_duration):
            try:
                g_duration = round(float(g_duration), 1)
            except ValueError:
                print('Duration has to be a positive value which shows the duration in hours (not 0)')
                return False
            if g_duration < 0:
                print('Duration has to be a positive value which shows the duration in hours (not 0)')
                return False
            return duration_setter(event_self, g_duration)
        return duration_validator

    @staticmethod
    def price_decorator_validate(price_setter):
        def price_validator(event_self, g_price):
            try:
                g_price = round(float(g_price), 2)
            except ValueError:
                print('Price has to be a positive number')
                return False
            if g_price < 0:
                print('Price has to be a positive number')
                return False
            return price_setter(event_self, g_price)
        return price_validator

    @staticmethod
    def sort_parameter_validate(sort_func):
        def sort_validator(col_self, g_param):
            sorting_dict = {'I': 'id',
                            'D': 'duration',
                            'P': 'price',
                            'R': 'rest_name',
                            'T': 'title',
                            'Da': 'date',
                            'Ti': 'time'}
            if g_param in sorting_dict:
                return sort_func(col_self, sorting_dict[g_param])
            else:
                print('No such parameter')
                return False
        return sort_validator

    @staticmethod
    def delete_validation(given_func):
        def delete_validator(col_self, g_param):
            if col_self.find_by_id(g_param):
                return given_func(col_self, int(g_param))
            else:
                print('No such ID')
                return False
        return delete_validator

    @staticmethod
    def find_by_id_validation(given_func):
        def find_validator(col_self, g_input):
            try:
                g_id = int(g_input)
                return given_func(col_self, g_id)
            except ValueError:
                print('ID has to be integer')
                return False
        return find_validator
