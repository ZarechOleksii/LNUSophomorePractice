import MySQLdb
from Collection import Collection
from flask import Flask, jsonify, request
from Event import Event
from Validation import Validation
import os
import hashlib

hello = Flask(__name__)
hello.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
hello.config['JSON_SORT_KEYS'] = False


@Validation.offset
def show_some(g_arr, g_offset, g_limit):
    event_from = g_offset * g_limit
    event_to = (g_offset + 1) * g_limit
    if event_from >= len(g_arr):
        return {'status': '777', 'message': 'No events on this page'}
    if event_to > len(g_arr):
        event_to = len(g_arr)
    to_return = []
    for x in range(event_from, event_to):
        to_return.append((g_arr[x]))
    return to_return


@hello.route('/api/logout', methods=['POST'])
def logout():
    global user_id
    if user_id == -1:
        return jsonify({'status': '400', 'message': 'Already logged out'})
    global all_events
    all_events = Collection([])
    user_id = -1
    return jsonify({'status': '200', 'message': 'Successfully logged out'})


@hello.route('/api/login', methods=['POST'])
def login():
    global all_events
    global user_id
    if user_id != -1:
        return jsonify({'status': '400', 'message': 'Already logged in'})
    if 'email' not in request.args or 'password' not in request.args:
        return jsonify({'status': '400', 'message': 'Need email and password'})

    cursor.execute("Select* From users where email = \'" + str(request.args['email']) + "\';")
    for x in cursor:
        salt_from_storage = x[4][:32]
        key_from_storage = x[4][32:]
        n_key = hashlib.pbkdf2_hmac('sha256', str(request.args['password']).encode('utf-8'), salt_from_storage, 100000)
        if key_from_storage == n_key:
            user_id = x[0]
            cursor.execute("Select* From events where user_id = " + str(user_id) + ";")
            parameters = ['id', 'title', 'rest_name', 'date', 'time', 'duration', 'price', 'user_id']
            collection = []
            iteration = 0
            for q in cursor:
                collection.append(dict())
                for z in range(0, len(parameters)):
                    collection[iteration][parameters[z]] = str(q[z])
                iteration += 1
            all_events = Collection(collection)
            return jsonify({'status': '200', 'message': 'Successfully logged in'})
        else:
            return jsonify({'status': '400', 'message': 'Wrong password'})
    return jsonify({'status': '400', 'message': 'No such email'})


@hello.route('/api/register', methods=['POST'])
def register():
    try:
        data = []
        args = ['first_name', 'last_name', 'email', 'password']
        args_validate = [Validation.name_validator, Validation.name_validator, Validation.email_validator,
                         Validation.pass_validator]
        errors = {}
        Validation.name_validator(request.args['first_name'])
        for x in range(0, len(args)):
            if args[x] in request.args:
                result = args_validate[x](request.args[args[x]])
                if result is True:
                    if x == 3:
                        key = hashlib.pbkdf2_hmac('sha256', str(request.args[args[x]]).encode('utf-8'), salt, 100000)
                        storage = salt + key
                        data.append(storage)
                    else:
                        data.append(request.args[args[x]])
                else:
                    errors[args[x]] = result
            else:
                errors[args[x]] = 'Missing'
        if not errors:
            columns = '(' + ', '.join(args) + ')'
            data = tuple(data)
            to_do = 'INSERT INTO users' + columns + ' VALUES (%s, %s, %s, %s)'
            cursor.execute(to_do, data)
            db.commit()
            return jsonify({'status': '200', 'message': 'Successful registration'})
        else:
            return jsonify({'status': '400', 'errors': errors})
    except MySQLdb.IntegrityError:
        return jsonify({'status': '400', 'message': 'Such email already registered'})


@hello.route('/events', methods=['GET'])
def print_all_and_search():
    if user_id == -1:
        return jsonify({'status': '200', 'message': 'Not logged in'})
    if 'what' in request.args:
        to_search = request.args['what']
        return jsonify(all_events.search3(to_search))
    elif 'sort_by' in request.args and 'sort_type' in request.args and 's' in request.args:
        found_events = Collection(all_events.search3(request.args['s']))
        to_return = found_events.sorting3(request.args['sort_by'], request.args['sort_type'])
    else:
        to_return = all_events.create_event_list()
    if 'limit' in request.args:
        if 'offset' in request.args:
            to_return = show_some(to_return, request.args['offset'], request.args['limit'])
        else:
            to_return = show_some(to_return, 0, request.args['limit'])
    return jsonify(to_return)


@hello.route('/events/<g_id>', methods=['GET'])
def print_one(g_id):
    if user_id == -1:
        return jsonify({'status': '200', 'message': 'Not logged in'})
    to_return = all_events.find_by_id(g_id)
    if to_return is not False:
        to_return = to_return.to_write()
    else:
        return jsonify({'status': '404', 'message': 'No such ID'})
    return jsonify(to_return)


@hello.route('/events/<g_id>', methods=['DELETE'])
def deleting_one(g_id):
    if user_id == -1:
        return jsonify({'status': '200', 'message': 'Not logged in'})
    if all_events.delete_id(g_id):
        cursor.execute("DELETE FROM Events WHERE id = " + str(g_id) + ";")
        db.commit()
        return jsonify({'status': '200', 'message': 'Successfully deleted'})
    else:
        return jsonify({'status': '404', 'message': 'No such ID'})


@hello.route('/events', methods=['POST'])
def add_one():
    if user_id == -1:
        return jsonify({'status': '200', 'message': 'Not logged in'})
    param_set = ('duration', 'price', 'rest_name', 'title', 'date', 'time')
    to_give = {}
    for x in param_set:
        if x not in request.args:
            return jsonify({'status': '400', 'message': 'Missing parameters'})
        else:
            to_give[x] = request.args[x]

    cursor.execute("select max(id) from events")
    for x in cursor:
        if x[0] is None:
            max_prev = 0
        else:
            max_prev = x[0]
        to_give['id'] = max_prev + 1
    to_give['user_id'] = user_id
    new_event = Event(to_give)
    if new_event.id == -1:
        return jsonify({'status': '400', 'message': 'wrong input', 'errors': new_event.errors})
    else:
        to_return = all_events.append(new_event)
        if to_return['status'] == '200':
            data = (to_give['id'], to_give['title'], to_give['rest_name'], to_give['date'], to_give['time'],
                    to_give['duration'], to_give['price'], to_give['user_id'])
            to_do = """INSERT INTO events
                    VALUES""" + str(data) + ';'
            cursor.execute(to_do)
            db.commit()
        return jsonify(to_return)


@hello.route('/events/<g_id>', methods=['PUT'])
def edit_one(g_id):
    if user_id == -1:
        return jsonify({'status': '200', 'message': 'Not logged in'})
    to_edit = all_events.find_by_id(g_id)
    if to_edit is not False:
        current = to_edit.to_write()
        for x in request.args:
            if x not in current:
                return jsonify({'status': '400', 'message': 'No such parameter'})
            if x == 'id':
                return jsonify({'status': '400', 'message': 'You cannot edit ID'})
            if x == 'user_id':
                return jsonify({'status': '400', 'message': 'You cannot edit user id'})
        result_dict = all_events.edit_entire_event(to_edit, request.args)
        if result_dict['status'] == '200':
            to_do = []
            for x in request.args:
                to_do.append(str(x + " = \'" + str(request.args[x]) + "\'"))
            cursor.execute("UPDATE events SET " + (', '.join(to_do)) + " WHERE id = " + g_id + ";")
            db.commit()
        return jsonify(result_dict)
    else:
        return jsonify({'status': '404', 'message': 'No such ID'})


if __name__ == '__main__':

    db = MySQLdb.connect("localhost", "root", "Az27061985", "test")
    cursor = db.cursor()
    user_id = -1
    all_events = Collection([])
    salt = os.urandom(32)
    hello.run()
    db.close()
