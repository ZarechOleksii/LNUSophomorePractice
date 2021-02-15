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
    def validate_float(given):
        try:
            float(given)
            return False
        except ValueError:
            return True

    @staticmethod
    def validate_bounds(given_index, given_list):
        try:
            given_list[given_index]
            return False
        except IndexError:
            return True

    @staticmethod
    def validate_title(given_title):
        for q in given_title:
            if q == '|' or q == '-' or q == ':':
                return False
        return given_title

    @staticmethod
    def validate_rest(given_rest_num):
        if Validation.validate_int(given_rest_num):
            return False
        given_rest_num = int(given_rest_num)
        if given_rest_num < 1 or given_rest_num > len(RestaurantName):
            return False
        return RestaurantName(given_rest_num)

    @staticmethod
    def validate_date(date):
        if Validation.validate_int(date[0]) or Validation.validate_int(date[1]) or Validation.validate_int(date[2]):
            return False
        try:
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
            return datetime.date(year, month, day)
        except ValueError:
            return False

    @staticmethod
    def validate_time(time):
        if Validation.validate_int(time[0]) or Validation.validate_int(time[1]):
            return False
        try:
            hour = int(time[0])
            minute = int(time[1])
            return datetime.time(hour, minute)
        except ValueError:
            return False

    @staticmethod
    def validate_duration(hours):
        if Validation.validate_float(hours):
            return False
        if float(hours) <= 0:
            return False
        return round(float(hours), 1)

    @staticmethod
    def validate_price(price):
        if Validation.validate_float(price):
            return False
        if float(price) < 0:
            return False
        return round(float(price), 2)

    @staticmethod
    def validate_file(name):
        try:
            val_file = open(name, 'r')
            val_file.close()
            return False
        except FileNotFoundError:
            return True

    @staticmethod
    def validate_id(g_id):
        if Validation.validate_int(g_id):
            return False
        else:
            if int(g_id) < 0:
                return False
            else:
                return int(g_id)
