from Validation import *
from Collection import Collection
from Event import Event
from RestaurantNames import RestaurantName
import datetime


def menu():
    print('\nA to add')
    print('D to delete')
    print('E to edit')
    print('S to sort')
    print('F to search')
    print('P to show all')
    print('Q to quit\n')


def edit_sort_menu():
    print('\nT - Title')
    print('R - Restaurant name')
    print('Da - Date')
    print('Ti - Starting time')
    print('D - Duration')
    print('P - Price\n')


def searching_by(parameter):
    if parameter == 'T':
        print('Sorting by titles')
    elif parameter == 'Da':
        print('Sorting by dates')
    elif parameter == 'Ti':
        print('Sorting by starting times')
    elif parameter == 'R':
        print('Sorting by restaurant names')
    elif parameter == 'D':
        print('Sorting by event durations')
    elif parameter == 'P':
        print('Sorting by ticket price')


def restaurants():
    for q in RestaurantName:
        print(q.value, '-', q.name)


def delete_from_collection(to_be_deleted, collection):
    if not Validation.validate_int(to_be_deleted):
        to_be_deleted = int(to_be_deleted) - 1
        if not Validation.validate_bounds(to_be_deleted, collection):
            Event.amount += -1
            return collection.delete_at(to_be_deleted)
        else:
            return 'Event was not deleted: no such ID'
    else:
        return 'Event was not deleted: ID is not an int'


def find_in_collection(to_be_found, collection):
    if not Validation.validate_int(to_be_found):
        return collection.search(to_be_found, True, False)
    elif not Validation.validate_float(to_be_found):
        return collection.search(to_be_found, False, True)
    else:
        return collection.search(to_be_found, False, False)


def overwrite(collection):
    writing = open('ToWrite.txt', 'w')
    writing.write(str(collection))
    writing.close()


def edit_object(parameter, instance):
    try:
        if parameter == 'T':
            new_title_n = create_title()
            instance.title = new_title_n
        elif parameter == 'R':
            new_rest_name = create_rest()
            instance.rest_name = new_rest_name
        elif parameter == 'Da':
            new_dates_n = create_date()
            hour = int(instance.date_time.strftime("%H"))
            minute = int(instance.date_time.strftime("%M"))
            instance.date_time = datetime.datetime(new_dates_n[0], new_dates_n[1], new_dates_n[2], hour, minute)
        elif parameter == 'Ti':
            new_times_n = create_time()
            year = int(instance.date_time.strftime("%Y"))
            month = int(instance.date_time.strftime("%m"))
            day = int(instance.date_time.strftime("%M"))
            instance.date_time = datetime.datetime(year, month, day, new_times_n[0], new_times_n[1])
        elif parameter == 'D':
            new_duration_n = create_duration()
            instance.duration = new_duration_n
        else:
            new_price_n = create_price()
            instance.price = new_price_n
        return True
    except RestNotInt:
        print('Restaurant number has to be an int value')
    except NoSuchRest:
        print('No such restaurant')
    except WrongDateFormat:
        print('Such date does not exist')
    except WrongTimeFormat:
        print('Starting hour has to be from 0 to 23, minute from 0 to 59')
    except DateNotInt:
        print('Date values need to be integers')
    except TimeNotInt:
        print('Time values need to be integers')
    except WrongDuration:
        print('Duration has to be a positive value which shows the duration in hours')
    except WrongPrice:
        print('Price has to be a positive number')
    return False


def create_title():
    print('Enter the title of the event:')
    return reading.readline().strip()


def create_rest():
    restaurants()
    print('Enter the number of the restaurant:')
    new_rest_n = reading.readline().strip()
    Validation.validate_rest(new_rest_n, RestaurantName)
    return RestaurantName(int(new_rest_n))


def create_date():
    print('Enter the year of the event:')
    new_year = reading.readline().strip()
    print('Enter the month of the event (number):')
    new_month = reading.readline().strip()
    print('Enter the day of the event (number):')
    new_day = reading.readline().strip()
    Validation.validate_date(new_year, new_month, new_day)
    return [int(new_year), int(new_month), int(new_day)]


def create_time():
    print('Enter when the event begins(hour):')
    new_hour = reading.readline().strip()
    print('Enter when the event begins(minute):')
    new_minute = reading.readline().strip()
    Validation.validate_time(new_hour, new_minute)
    return [int(new_hour), int(new_minute)]


def create_duration():
    print('Enter the duration of the event in hours:')
    new_duration_n = reading.readline().strip()
    Validation.validate_duration(new_duration_n)
    new_duration_n = round(float(new_duration_n), 1)
    return new_duration_n


def create_price():
    print('Enter the price in $:')
    new_price_n = reading.readline().strip()
    Validation.validate_price(new_price_n)
    new_price_n = round(float(new_price_n), 2)
    return new_price_n


reading = open('ToRead.txt', 'r')
all_events = Collection()
while True:
    menu()
    action = reading.readline().strip()
    if action == 'Q':
        break
    elif action == 'A':
        try:
            new_title = create_title()
            new_rest = create_rest()
            new_date = create_date()
            new_time = create_time()
            n_date_time = datetime.datetime(new_date[0], new_date[1], new_date[2], new_time[0], new_time[1])
            new_duration = create_duration()
            new_price = create_price()

            new_event = Event(new_title, new_rest, n_date_time, new_duration, new_price)
            all_events.append(new_event)

            print(new_event)
            print('New object successfully created')
            overwrite(all_events)
        except RestNotInt:
            print('Restaurant number has to be an int value')
        except NoSuchRest:
            print('No such restaurant')
        except WrongDateFormat:
            print('Such date does not exist')
        except WrongTimeFormat:
            print('Starting hour has to be from 0 to 23, minute from 0 to 59')
        except DateNotInt:
            print('Date values need to be integers')
        except TimeNotInt:
            print('Time values need to be integers')
        except WrongDuration:
            print('Duration has to be a positive value which shows the duration in hours')
        except WrongPrice:
            print('Price has to be a positive number')

    elif action == 'E':
        print('Enter the ID of the element you want to edit:\n')
        obj_to_edit = reading.readline().strip()
        if not Validation.validate_int(obj_to_edit):
            obj_to_edit = int(obj_to_edit) - 1
            if not Validation.validate_bounds(obj_to_edit, all_events):
                print(all_events[obj_to_edit])
                print('\nEnter the parameter you want to edit:')
                edit_sort_menu()
                param = reading.readline().strip()
                if param == 'T' or param == 'Ti' or param == 'Da' or param == 'D' or param == 'P' or param == 'R':
                    if edit_object(param, all_events[obj_to_edit]):
                        overwrite(all_events)
                        print('Event with ID', obj_to_edit + 1, 'was successfully edited')
                    else:
                        print('Event with ID', obj_to_edit + 1, 'was left unedited')
                else:
                    print('No such parameter')
            else:
                print('No event with such ID')
        else:
            print('ID has to be an int')

    elif action == 'F':
        print('Enter what you find to find: ')
        to_find = reading.readline().strip()
        print('Looking for', to_find)
        print(find_in_collection(to_find, all_events))

    elif action == 'D':
        print(all_events)
        print('Enter the ID of the element you want to delete:')
        to_delete = reading.readline().strip()
        print(delete_from_collection(to_delete, all_events))
        overwrite(all_events)

    elif action == 'S':
        print('Enter the letter of the sorting parameter:')
        edit_sort_menu()
        param = reading.readline().strip()
        if param == 'T' or param == 'Ti' or param == 'Da' or param == 'D' or param == 'P' or param == 'R':
            searching_by(param)
            print(all_events.sorting(param))
        else:
            print('No such option')

    elif action == 'P':
        print(all_events)

    else:
        print('No such option')
reading.close()
