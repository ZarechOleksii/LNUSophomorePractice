from Validation import Validation


class Event:
    to_return_dict = {'ID: ': 'id',
                      'Title: ': 'title',
                      'Restaurant name: ': 'rest_name',
                      'Date: ': 'date',
                      'Starting time: ': 'time',
                      'Duration: ': 'duration',
                      'Price: ': 'price'}
    setters = {'id': 'set_id',
               'title': 'set_title',
               'rest_name': 'set_rest',
               'date': 'set_date',
               'time': 'set_time',
               'duration': 'set_duration',
               'price': 'set_price',
               'user_id': 'set_user'}

    def __init__(self, init_dict):
        created = True
        self.errors = dict()
        for q in self.setters:
            if not self.edit_value(q, init_dict[q]):
                created = False
                self.errors[q] = 'Wrong Input'
        if not created:
            self.id = -1

    def __str__(self):
        to_return = ''
        for q in self.to_return_dict:
            to_return += q + str(getattr(self, self.to_return_dict[q])) + '\n'
        return to_return

    def edit_value(self, parameter, to_edit):
        return getattr(self, self.setters[parameter])(to_edit)

    def to_write(self):
        to_return = dict()
        for q in self.setters:
            if q == 'rest_name':
                to_return[q] = (str(getattr(self, q).name))
            else:
                to_return[q] = (str(getattr(self, q)))
        return to_return

    @Validation.id_decorator_validate
    def set_id(self, new_id):
        setattr(self, 'id', new_id)
        return True

    @Validation.title_decorator_validate
    def set_title(self, new_title):
        setattr(self, 'title', new_title)
        return True

    @Validation.rest_decorator_validate
    def set_rest(self, new_rest):
        setattr(self, 'rest_name', new_rest)
        return True

    @Validation.date_decorator_validate
    def set_date(self, new_date):
        setattr(self, 'date', new_date)
        return True

    @Validation.time_decorator_validate
    def set_time(self, new_time):
        setattr(self, 'time', new_time)
        return True

    @Validation.duration_decorator_validate
    def set_duration(self, new_duration):
        setattr(self, 'duration', new_duration)
        return True

    @Validation.price_decorator_validate
    def set_price(self, new_price):
        setattr(self, 'price', new_price)
        return True

    @Validation.user_decorator_validate
    def set_user(self, new_user):
        setattr(self, 'user_id', new_user)
        return True
