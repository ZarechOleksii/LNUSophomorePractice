from Validation import Validation


class Event:
    to_return_dict = {'ID: ': 'id',
                      'Title: ': 'title',
                      'Restaurant name: ': 'rest_name',
                      'Date: ': 'date',
                      'Starting time: ': 'time',
                      'Duration: ': 'duration',
                      'Price: ': 'price'}
    validation_dict = {'id': 'validate_id',
                       'title': 'validate_title',
                       'rest_name': 'validate_rest',
                       'date': 'validate_date',
                       'time': 'validate_time',
                       'duration': 'validate_duration',
                       'price': 'validate_price'}
    error_messages = {'id': 'ID has to be a positive integer',
                      'title': 'Title should not contain symbols "-", "|" and ":"',
                      'rest_name': 'Restaurant number has to be an int value which is present in restaurant list',
                      'date': 'Date values need to be integers of existing date',
                      'time': 'Time values need to be integers from 0 to 23 for hours and from 0 to 59 for minutes',
                      'duration': 'Duration has to be a positive value which shows the duration in hours (not 0)',
                      'price': 'Price has to be a positive number'}

    def __init__(self, init_dict):
        self.id = 0
        to_create = True
        for q in self.validation_dict:
            init_dict[q] = (getattr(Validation, self.validation_dict[q])(init_dict[q]))
        for q in init_dict:
            if init_dict[q] is False:
                to_create = False
                print('\t', self.error_messages[q])
        if to_create:
            for q in init_dict:
                setattr(self, q, init_dict[q])

    def __str__(self):
        to_return = ''
        for q in self.to_return_dict:
            to_return += q + str(getattr(self, self.to_return_dict[q])) + '\n'
        return to_return

    def edit_value(self, parameter, to_edit):
        to_edit = getattr(Validation, self.validation_dict[parameter])(to_edit)
        if to_edit is False:
            print(self.error_messages[parameter])
            return False
        else:
            setattr(self, parameter, to_edit)
            return True

    def to_write(self):
        to_return = []
        for q in self.validation_dict:
            if q == 'rest_name':
                to_return.append(str(getattr(self, q).value))
            else:
                to_return.append(str(getattr(self, q)))
        return '| '.join(to_return)
