from Validation import Validation


class Event:
    setters = {'id': 'set_id',
               'title': 'set_title',
               'rest_name': 'set_rest',
               'date': 'set_date',
               'time': 'set_time',
               'duration': 'set_duration',
               'price': 'set_price',
               'user_id': 'set_user',
               'amount': 'set_amount'}

    def __init__(self, init_dict):
        created = True
        self.errors = dict()
        for q in self.setters:
            if not self.edit_value(q, init_dict[q]):
                created = False
                self.errors[q] = 'Wrong Input'
        if not created:
            self.id = -1

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

    @Validation.id_decorator_validate
    def set_amount(self, new_amount):
        setattr(self, 'amount', new_amount)
        return True

    def edit_entire_event(self, g_dict):
        backup = self.to_write()
        all_good = True
        to_return = dict()
        errors = dict()
        for x in g_dict:
            if not self.edit_value(x, g_dict[x]):
                if all_good is True:
                    all_good = False
                    to_return['status'] = '400'
                    to_return['message'] = 'Wrong Input'
                errors[x] = 'Wrong input'
                to_return['errors'] = errors
        if not all_good:
            self.edit_entire_event(backup)
        else:
            to_return['status'] = '200'
            to_return['message'] = 'Customer has been successfully updated.'
            to_return['customer'] = self.to_write()
        return to_return
