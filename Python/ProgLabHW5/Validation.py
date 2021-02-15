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
        def file_validator(col_self):
            try:
                file_name = input('Enter file name: ')
                val_file = open(file_name, 'r')
                val_file.close()
                return col_init(col_self, file_name)
            except FileNotFoundError:
                return file_validator(col_self)
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
