import datetime


class RestNotInt(Exception):
    pass


class NoSuchRest(Exception):
    pass


class DateNotInt(Exception):
    pass


class WrongDateFormat(Exception):
    pass


class TimeNotInt(Exception):
    pass


class WrongTimeFormat(Exception):
    pass


class WrongDuration(Exception):
    pass


class WrongPrice(Exception):
    pass


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
    def validate_rest(given_rest_num, g_restaurants):
        if Validation.validate_int(given_rest_num):
            raise RestNotInt
        given_rest_num = int(given_rest_num)
        if given_rest_num < 1 or given_rest_num > len(g_restaurants):
            raise NoSuchRest

    @staticmethod
    def validate_date(year, month, day):
        if Validation.validate_int(year) or Validation.validate_int(month) or Validation.validate_int(day):
            raise DateNotInt
        try:
            year = int(year)
            month = int(month)
            day = int(day)
            datetime.datetime(year, month, day)
        except ValueError:
            raise WrongDateFormat

    @staticmethod
    def validate_time(hour, minute):
        if Validation.validate_int(hour) or Validation.validate_int(minute):
            raise TimeNotInt
        try:
            hour = int(hour)
            minute = int(minute)
            datetime.datetime(2020, 1, 1, hour, minute)
        except ValueError:
            raise WrongTimeFormat

    @staticmethod
    def validate_duration(hours):
        if Validation.validate_float(hours):
            raise WrongDuration
        if float(hours) <= 0:
            raise WrongDuration

    @staticmethod
    def validate_price(price):
        if Validation.validate_float(price):
            raise WrongPrice
        if float(price) < 0:
            raise WrongPrice
