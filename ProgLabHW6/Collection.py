from Event import Event
from Validation import Validation
from Caretaker import Caretaker
from Momento import Momento


class Collection:

    search_dict = {'id': 'ID',
                   'duration': 'duration',
                   'price': 'price',
                   'rest_name': 'restaurant name',
                   'title': 'title',
                   'date': 'starting date',
                   'time': 'starting time'}
    list_to_read = ['id', 'title', 'rest_name', 'date', 'time', 'duration', 'price']
    open_file = ''

    @Validation.file_name_decorator_validate
    def __init__(self, file_name):
        line = 0
        self.all_events = []
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
            dict_to_read['date'] = dict_to_read['date'].split('-')
            dict_to_read['time'] = dict_to_read['time'].split(':')
            new_event = Event(dict_to_read)
            if new_event.id != -1:
                self.all_events.append(new_event)
                print('Line', line, 'initialized properly')
            else:
                print('Line', line, 'was not initialized properly')
        reading.close()
        self.history = Caretaker()
        self.history.new_action(Momento(self.all_events), 'Initialization')

    def append(self, given_event):
        self.all_events.append(given_event)
        self.history.new_action(Momento(self.all_events), ('Added new element with ID ' + str(given_event.id)))

    def __len__(self):
        return len(self.all_events)

    def __getitem__(self, item):
        return self.all_events[item]

    def __str__(self):
        to_return_all = ''
        for q in range(0, len(self.all_events)):
            to_return_all += str(self.all_events[q])
        return to_return_all

    def find_by_id(self, g_id):
        for q in range(0, len(self.all_events)):
            if g_id == self.all_events[q].id:
                return self.all_events[q]

    def delete_id(self, g_id):
        for q in range(0, len(self.all_events)):
            if g_id == self.all_events[q].id:
                self.all_events.pop(q)
                self.history.new_action(Momento(self.all_events), ('Deleted element with ID ' + str(g_id)))
                return True
        return False

    def sorting2(self, by_what):
        if by_what == 'title':
            self.all_events = sorted(self.all_events, key=lambda b: getattr(b, by_what).lower())
        else:
            self.all_events = sorted(self.all_events, key=lambda b: getattr(b, by_what))
        self.history.new_action(Momento(self.all_events), ('Sorted by ' + self.search_dict[by_what]))

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
        for q in self.search_dict:
            for j in range(0, len(self)):
                if self.search_loop(looking_for, str(getattr(self.all_events[j], q))):
                    to_return_found += 'Event with ID ' + str(self.all_events[j].id) + ' has '
                    to_return_found += self.search_dict[q] + ' ' + str(getattr(self.all_events[j], q)) + '\n'
        return to_return_found

    def rewrite(self):
        to_write = ''
        for q in self.all_events:
            to_write += q.to_write() + '\n'
        writing = open(self.open_file, 'w')
        writing.write(to_write)
        writing.close()

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

    def undo(self):
        action = self.history.undo()
        if action is not False:
            self.all_events = action.get_momento_value()

    def redo(self):
        action = self.history.redo()
        if action is not False:
            self.all_events = action.get_momento_value()
