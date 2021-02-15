from Event import Event
from Validation import Validation
from Caretaker import Caretaker
from Momento import Momento
import json


class Collection:

    search_dict = {'id': 'ID',
                   'duration': 'duration',
                   'price': 'price',
                   'rest_name': 'restaurant name',
                   'title': 'title',
                   'date': 'starting date',
                   'time': 'starting time'}
    open_file = ''

    # @Validation.file_name_decorator_validate
    def __init__(self, g_arr):
        self.all_events = []
        for x in g_arr:
            new_event = Event(x)
            if new_event.id != -1:
                self.all_events.append(new_event)
        self.history = Caretaker()
        self.history.new_action(Momento(self.all_events), 'Initialization')

    def append(self, given_event):
        if not self.present(given_event.id):
            self.all_events.append(given_event)
            self.history.new_action(Momento(self.all_events), ('Added new element with ID ' + str(given_event.id)))
            return {'status': '200', 'message': 'Successfully created'}
        else:
            return {'status': '400', 'message': 'ID already exists'}

    def __len__(self):
        return len(self.all_events)

    def __getitem__(self, item):
        return self.all_events[item]

    def __str__(self):
        to_return_all = ''
        for q in range(0, len(self.all_events)):
            to_return_all += str(self.all_events[q])
        return to_return_all

    @Validation.find_by_id_validation
    def find_by_id(self, g_id):
        for q in range(0, len(self.all_events)):
            if g_id == self.all_events[q].id:
                return self.all_events[q]
        return False

    @Validation.delete_validation
    def delete_id(self, g_id):
        for q in range(0, len(self.all_events)):
            if g_id == self.all_events[q].id:
                self.all_events.pop(q)
                self.history.new_action(Momento(self.all_events), ('Deleted element with ID ' + str(g_id)))
                return True
        return False

    @Validation.sort_parameter_validate
    def sorting2(self, by_what):
        if by_what == 'title':
            self.all_events = sorted(self.all_events, key=lambda b: getattr(b, by_what).lower())
        else:
            self.all_events = sorted(self.all_events, key=lambda b: getattr(b, by_what))
        self.history.new_action(Momento(self.all_events), ('Sorted by ' + self.search_dict[by_what]))
        return True

    @Validation.sort_parameter_validate2
    def sorting3(self, by_what, sort_type):
        if by_what == 'title':
            self.all_events = sorted(self.all_events, key=lambda b: getattr(b, by_what).lower())
        else:
            self.all_events = sorted(self.all_events, key=lambda b: getattr(b, by_what))
        if sort_type == 'desc':
            self.all_events.reverse()
        return self.create_event_list()

    @staticmethod
    def search_loop(to_look_for, to_be_checked):
        checker = 0
        for w in range(0, len(to_be_checked)):
            if to_be_checked[w] == to_look_for[checker]:
                checker += 1
            else:
                checker = 0
            if checker == len(to_look_for):
                return True
        return False

    def search2(self, looking_for):
        to_return_found = ''
        if len(looking_for) > 0:
            for q in self.search_dict:
                for j in range(0, len(self)):
                    if self.search_loop(looking_for, str(getattr(self.all_events[j], q))):
                        to_return_found += 'Event with ID ' + str(self.all_events[j].id) + ' has '
                        to_return_found += self.search_dict[q] + ' ' + str(getattr(self.all_events[j], q)) + '\n'
        return to_return_found

    def search3(self, looking_for):
        to_return_found = []
        if len(looking_for) > 0:
            for j in range(0, len(self)):
                for q in self.search_dict:
                    if self.search_loop(looking_for, str(getattr(self.all_events[j], q))):
                        to_return_found.append(self.all_events[j].to_write())
                        break
        else:
            return self.create_event_list()
        return to_return_found

    def create_event_list(self):
        to_return = []
        for q in self.all_events:
            to_return.append(q.to_write())
        return to_return

    def rewrite(self):
        to_write = self.create_event_list()
        for q in range(0, len(to_write)):
            to_write[q] = (to_write[q]['id'], to_write[q]['title'], to_write[q]['rest_name'], to_write[q]['date'],
                           to_write[q]['time'], to_write[q]['duration'], to_write[q]['price'])
        return to_write

    def present(self, given_id):
        for q in range(0, len(self.all_events)):
            if given_id == self.all_events[q].id:
                return True
        return False

    def show_history(self):
        return self.history

    def edit_one(self, event_to_edit, g_param, g_value):
        if event_to_edit.edit_value(g_param, g_value):
            self.history.new_action(Momento(self.all_events), ('Edited element with ID' + str(event_to_edit.id)))
            return True
        else:
            return False

    def edit_entire_event(self, event_to_edit, g_dict):
        backup = event_to_edit.to_write()
        all_good = True
        to_return = dict()
        errors = dict()
        for x in g_dict:
            if x == 'id':
                if self.present(g_dict[x]):
                    all_good = False
                    to_return['status'] = '400'
                    to_return['message'] = 'Wrong Input'
                    errors[x] = 'ID occupied'
            if not event_to_edit.edit_value(x, g_dict[x]):
                if all_good is True:
                    all_good = False
                    to_return['status'] = '400'
                    to_return['message'] = 'Wrong Input'
                errors[x] = 'Wrong input'
                to_return['errors'] = errors
        if not all_good:
            self.edit_entire_event(event_to_edit, backup)
        else:
            to_return['status'] = '200'
            to_return['message'] = 'Customer has been successfully updated.'
            to_return['customer'] = event_to_edit.to_write()
        return to_return

    def undo(self):
        action = self.history.undo()
        if action is not False:
            self.all_events = action.get_momento_value()
            return True
        return False

    def redo(self):
        action = self.history.redo()
        if action is not False:
            self.all_events = action.get_momento_value()
            return True
        return False
