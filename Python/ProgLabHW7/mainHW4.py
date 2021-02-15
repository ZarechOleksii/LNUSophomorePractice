from Validation import *
from Collection import Collection
from Event import Event
from RestaurantNames import RestaurantName


def menu():
    print('\nA to add')
    print('D to delete')
    print('E to edit')
    print('S to sort')
    print('F to search')
    print('P to show all')
    print('H to show last 5 actions')
    print('U to undo')
    print('R to redo')
    print('Q to quit\n')


def restaurants():
    for q in RestaurantName:
        print(q.value, '-', q.name)


all_events = Collection('')

while True:
    menu()
    action = input()
    if action == 'Q':
        break
    elif action == 'A':
        initial_dict = dict()
        initial_dict['id'] = input('Enter the ID of the event (positive integer): ')
        initial_dict['title'] = input('Enter the title of the event (characters "|", ":" and "-" are forbidden): ')
        restaurants()
        initial_dict['rest_name'] = input('Enter the number of the restaurant: ')
        new_year = input('Enter the year of the event: ')
        new_month = input('Enter the month of the event (number): ')
        new_day = input('Enter the day of the event (number): ')
        initial_dict['date'] = [new_year, new_month, new_day]
        new_hour = input('Enter when the event begins(hour): ')
        new_minute = input('Enter when the event begins(minute): ')
        initial_dict['time'] = [new_hour, new_minute]
        initial_dict['duration'] = input('Enter event duration in hours: ')
        initial_dict['price'] = input('Enter price in $: ')

        new_event = Event(initial_dict)
        if new_event.id != -1:
            all_events.append(new_event)
            print(new_event)
            print('New object successfully created')
            all_events.rewrite()
        else:
            print('New object was not created')

    elif action == 'E':
        print(all_events)
        print('Enter the ID of the element you want to edit:\n')
        id_to_edit = input()
        obj_to_edit = all_events.find_by_id(id_to_edit)
        if obj_to_edit is not False:
            print(obj_to_edit)
            print('\nEnter the parameter you want to edit:')
            print('T - Title')
            print('R - Restaurant name')
            print('Da - Date')
            print('Ti - Starting time')
            print('D - Duration')
            print('P - Price\n')
            edit_dict = {'D': 'duration',
                         'P': 'price',
                         'R': 'rest_name',
                         'T': 'title',
                         'Da': 'date',
                         'Ti': 'time'}
            param = input()
            if param in edit_dict:
                if param == 'Da':
                    new_value = list()
                    new_value.append(input('Enter the year of the event: '))
                    new_value.append(input('Enter the month of the event (number): '))
                    new_value.append(input('Enter the day of the event (number): '))
                elif param == 'Ti':
                    new_value = list()
                    new_value.append(input('Enter when the event begins(hour): '))
                    new_value.append(input('Enter when the event begins(minute): '))
                else:
                    new_value = input('Enter new value: ')
                if all_events.edit_one(obj_to_edit, edit_dict[param], new_value):
                    all_events.rewrite()
                    print('Event with ID', id_to_edit, 'was successfully edited')
                else:
                    print('Event with ID', id_to_edit, 'was left unedited')
            else:
                print('No such parameter')

    elif action == 'F':
        print('Enter what you find to find: ')
        to_find = input()
        print('Looking for', to_find)
        print(all_events.search2(to_find))

    elif action == 'D':
        print(all_events)
        print('Enter the ID of the element you want to delete:')
        to_delete = input()
        if all_events.delete_id(to_delete):
            print('Element with ID', to_delete, 'was removed')
            all_events.rewrite()

    elif action == 'S':
        print('\nEnter the letter of the sorting parameter:')
        print('T - Title')
        print('I - ID')
        print('R - Restaurant name')
        print('Da - Date')
        print('Ti - Starting time')
        print('D - Duration')
        print('P - Price\n')
        param = input()
        if all_events.sorting2(param):
            print(all_events)
            all_events.rewrite()

    elif action == 'P':
        print(all_events)

    elif action == 'H':
        print(all_events.show_history())

    elif action == 'U':
        all_events.undo()
        all_events.rewrite()

    elif action == 'R':
        all_events.redo()
        all_events.rewrite()

    else:
        print('No such option')
