
class Collection:
    def __init__(self):
        self.all_events = []

    def append(self, given_event):
        self.all_events.append(given_event)

    def __len__(self):
        return len(self.all_events)

    def __getitem__(self, item):
        return self.all_events[item]

    def __str__(self):
        to_return_all = ''
        for q in range(0, len(self.all_events)):
            to_return_all += '\n' + str(self.all_events[q]) + '\n'
        return to_return_all

    def delete_at(self, g_index):
        if (g_index + 1) == len(self):
            self.all_events.pop()
        else:
            self.all_events[g_index] = self.all_events.pop()
            self.all_events[g_index].id = g_index + 1
        return 'Event with ID ' + str(g_index + 1) + ' removed'

    def sorting(self, by_what):
        sort_parameter = []
        if by_what == 'D':
            for q in range(0, len(self)):
                sort_parameter.append(self.all_events[q].duration)
        if by_what == 'P':
            for q in range(0, len(self)):
                sort_parameter.append(float(self.all_events[q].price[0:-2]))
        if by_what == 'Ti':
            for q in range(0, len(self)):
                time_string = self.all_events[q].date_time.strftime("%H") + self.all_events[q].date_time.strftime("%M")
                sort_parameter.append(time_string)
        if by_what == 'Da':
            for q in range(0, len(self)):
                date_string = self.all_events[q].date_time.strftime("%Y")
                date_string += self.all_events[q].date_time.strftime("%m")
                date_string += self.all_events[q].date_time.strftime("%d")
                sort_parameter.append(date_string)
        if by_what == 'R':
            for q in range(0, len(self)):
                sort_parameter.append(self.all_events[q].rest_name.name)
        if by_what == 'T':
            for q in range(0, len(self)):
                sort_parameter.append(self.all_events[q].title)
        paired = zip(sort_parameter, self.all_events)
        if by_what == 'R' or by_what == 'T':
            paired = sorted(paired, key=lambda a: (a[0].lower()))
        else:
            paired = sorted(paired)
        result = ''
        for q in paired:
            result += '\n' + str(q[1]) + '\n'
        return result

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

    def search(self, looking_for, is_int, is_float):
        to_return_found = ''
        if is_int:
            for q in range(0, len(self)):
                to_check = str(self.all_events[q].id)
                if self.search_loop(looking_for, to_check):
                    to_return_found += 'There is an event with ID ' + to_check + '\n'

        for q in range(0, len(self)):
            to_check = self.all_events[q].title
            if self.search_loop(looking_for, to_check):
                to_return_found += 'Event with ID ' + str(self.all_events[q].id) + ' has title ' + to_check + '\n'

        if not is_int and not is_float:
            for q in range(0, len(self)):
                to_check = self.all_events[q].rest_name.name
                if self.search_loop(looking_for, to_check):
                    to_return_found += 'Event with ID ' + str(self.all_events[q].id)
                    to_return_found += ' has restaurant name ' + to_check + '\n'

        if is_int:
            lower_bound = 0
            higher_bound = 5
        elif not is_float:
            lower_bound = 5
            higher_bound = 7
        else:
            lower_bound, higher_bound = 0, 0
        for x in range(lower_bound, higher_bound):
            if x == 0:
                part_of_date_time = "%d"
                part_of_return = ' has day of month '
            elif x == 1:
                part_of_date_time = "%m"
                part_of_return = ' has month with number '
            elif x == 2:
                part_of_date_time = "%Y"
                part_of_return = ' has year '
            elif x == 3:
                part_of_date_time = "%H"
                part_of_return = ' starts at hour '
            elif x == 4:
                part_of_date_time = "%M"
                part_of_return = ' starts at minute '
            elif x == 5:
                part_of_date_time = "%A"
                part_of_return = ' has weekday '
            else:
                part_of_date_time = "%B"
                part_of_return = ' has month '
            for q in range(0, len(self)):
                to_check = self.all_events[q].date_time.strftime(part_of_date_time)
                if self.search_loop(looking_for, to_check):
                    to_return_found += 'Event with ID ' + str(self.all_events[q].id)
                    to_return_found += part_of_return + to_check + '\n'

        if is_float or is_int:
            for q in range(0, len(self)):
                to_check = str(self.all_events[q].duration)
                if self.search_loop(looking_for, to_check):
                    to_return_found += 'Event with ID ' + str(self.all_events[q].id)
                    to_return_found += ' has duration ' + to_check + '\n'

        for q in range(0, len(self)):
            to_check = self.all_events[q].price
            if self.search_loop(looking_for, to_check):
                to_return_found += 'Event with ID ' + str(self.all_events[q].id)
                to_return_found += ' has price ' + to_check + '\n'
        return to_return_found
