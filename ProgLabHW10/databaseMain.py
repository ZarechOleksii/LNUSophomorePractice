import MySQLdb
from Collection import Collection
from flask import Flask, jsonify, request
from Event import Event
from Validation import Validation
import os
import hashlib
import datetime as dt

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
    global access_level
    if user_id == -1:
        return jsonify({'status': '400', 'message': 'Already logged out'})
    user_id = -1
    access_level = 'user'
    return jsonify({'status': '200', 'message': 'Successfully logged out'})


@hello.route('/api/login', methods=['POST'])
def login():
    global user_id
    global access_level
    global current_ord
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
            access_level = x[5]
            cursor.execute("Select* From orders where user_id = " + str(user_id) + ";")
            parameters_ord = ['user_id', 'item_id', 'amount', 'date']
            collection_ord = []
            iteration_ord = 0
            for b in cursor:
                collection_ord.append(dict())
                for r in range(0, len(parameters_ord)):
                    collection_ord[iteration_ord][parameters_ord[r]] = str(b[r])
                iteration_ord += 1
            current_ord = collection_ord
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
            args.append('access')
            data.append('user')
            columns = '(' + ', '.join(args) + ')'
            data = tuple(data)
            to_do = 'INSERT INTO users' + columns + ' VALUES (%s, %s, %s, %s, %s)'
            cursor.execute(to_do, data)
            db.commit()
            return jsonify({'status': '200', 'message': 'Successful registration'})
        else:
            return jsonify({'status': '400', 'errors': errors})
    except MySQLdb.IntegrityError:
        return jsonify({'status': '400', 'message': 'Such email already registered'})


@hello.route('/events', methods=['GET'])
def print_all_and_search():
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
    if access_level != 'admin':
        return jsonify({'status': '403', 'message': 'Forbidden'})
    global current_ord
    if all_events.delete_id(g_id):
        cursor.execute("DELETE FROM Events WHERE id = " + str(g_id) + ";")
        cursor.execute("DELETE FROM orders WHERE item_id = " + str(g_id) + ";")
        new_ord = []
        for x in current_ord:
            if x['item_id'] != str(g_id):
                new_ord.append(x)
        current_ord = new_ord
        db.commit()
        return jsonify({'status': '200', 'message': 'Successfully deleted'})
    else:
        return jsonify({'status': '404', 'message': 'No such ID'})


@hello.route('/events', methods=['POST'])
def add_one():
    if user_id == -1:
        return jsonify({'status': '200', 'message': 'Not logged in'})
    if access_level != 'admin':
        return jsonify({'status': '403', 'message': 'Forbidden'})
    param_set = ('duration', 'price', 'rest_name', 'title', 'date', 'time', 'amount')
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
                    to_give['duration'], to_give['price'], to_give['user_id'], to_give['amount'])
            to_do = """INSERT INTO events
                    VALUES""" + str(data) + ';'
            cursor.execute(to_do)
            db.commit()
        return jsonify(to_return)


@hello.route('/events/<g_id>', methods=['PUT'])
def edit_one(g_id):
    if user_id == -1:
        return jsonify({'status': '200', 'message': 'Not logged in'})
    if access_level != 'admin':
        return jsonify({'status': '403', 'message': 'Forbidden'})
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


@hello.route('/orders', methods=['GET'])
def print_all():
    if user_id == -1:
        return jsonify({'status': '200', 'message': 'Not logged in'})
    to_return = current_ord
    if 'limit' in request.args:
        if 'offset' in request.args:
            to_return = show_some(to_return, request.args['offset'], request.args['limit'])
        else:
            to_return = show_some(to_return, 0, request.args['limit'])
    return jsonify(to_return)


@hello.route('/orders/<g_id>', methods=['GET'])
def print_one_order(g_id):
    if user_id == -1:
        return jsonify({'status': '200', 'message': 'Not logged in'})
    to_return = []
    for x in current_ord:
        if x['item_id'] == str(g_id):
            to_return.append(x)
    if len(to_return) != 0:
        return jsonify(to_return)
    else:
        return jsonify({'status': '404', 'message': 'No such ID'})


@hello.route('/orders', methods=['POST'])
def add_one_order():
    if user_id == -1:
        return jsonify({'status': '200', 'message': 'Not logged in'})
    if 'item_id' not in request.args:
        return jsonify({'status': '400', 'message': 'Need item ID'})
    else:
        cursor.execute("Select* From events where id = " + str(request.args['item_id']))
        for x in cursor:
            if x[0] is None:
                return jsonify({'status': '404', 'message': 'No item with such id'})
            if x[8] == 0:
                return jsonify({'status': '400', 'message': 'No items left in stock'})
            to_do = "update events set amount = \'" + str(x[8] - 1) + "\' where id = " + str(request.args['item_id'])
            cursor.execute(to_do)
            all_events.find_by_id(int(request.args['item_id'])).amount -= 1
            for r in current_ord:
                if r['user_id'] == str(user_id):
                    if r['item_id'] == str(request.args['item_id']):
                        r['date'] = str(dt.datetime.now().date())
                        r['amount'] = str(int(r['amount']) + 1)
                        to_do = "Update orders set amount = \'" + str(r['amount']) + '\', date' \
                                ' = \'' + str(r['date']) + '\' where user_id = \'' + str(r['user_id']) + '\' and ' \
                                'item_id = \'' + str(r['item_id']) + '\';'
                        cursor.execute(to_do)
                        db.commit()
                        return jsonify({'status': '200', 'message': 'Successfully updated existing order',
                                        'order': r})
            new_order = {'user_id': str(user_id), 'item_id': str(request.args['item_id']),
                         'amount': '1', 'date': str(dt.datetime.now().date())}
            current_ord.append(new_order)
            new_order_tup = []
            for r in new_order:
                new_order_tup.append(new_order[r])
            new_order_tup = tuple(new_order_tup)
            cursor.execute("INSERT INTO orders VALUES" + str(new_order_tup) + ';')
            db.commit()
            return jsonify({'status': '200', 'message': 'Successfully added new order', 'order': new_order})
        return jsonify({'status': '404', 'message': 'No item with such id'})


@hello.route('/users/<g_id>', methods=['DELETE'])
def deleting_one_user(g_id):
    if user_id == -1:
        return jsonify({'status': '200', 'message': 'Not logged in'})
    if access_level != 'admin':
        return jsonify({'status': '403', 'message': 'Forbidden'})
    cursor.execute('select* from users where id = ' + g_id)
    for x in cursor:
        if x[5] == 'admin':
            return jsonify({'status': '400', 'message': 'Cannot delete admin'})
        cursor.execute('select item_id, amount from orders where user_id = ' + g_id)
        for c in cursor:
            cursor.execute('select amount from events where id = ' + str(c[0]))
            for j in cursor:
                new_amount = j[0] + c[1]
                all_events.find_by_id(int(c[0])).amount = new_amount
                cursor.execute('update events set amount = ' + str(new_amount) + ' where id = ' + str(c[0]))
        cursor.execute('delete from users where id = ' + g_id)
        cursor.execute('delete from orders where user_id = ' + g_id)
        db.commit()
        return jsonify({'status': '200', 'message': 'Customer and his orders deleted'})
    return jsonify({'status': '404', 'message': 'No such user'})


@hello.route('/users/<g_id>', methods=['PUT'])
def edit_one_user(g_id):
    if user_id == -1:
        return jsonify({'status': '200', 'message': 'Not logged in'})
    if access_level != 'admin':
        return jsonify({'status': '403', 'message': 'Forbidden'})
    cursor.execute('select* from users where id = ' + g_id)
    for x in cursor:
        if x[5] == 'admin':
            return jsonify({'status': '400', 'message': 'Cannot edit admin'})
        data = []
        column = []
        args = ['first_name', 'last_name', 'email', 'password']
        args_validate = {'first_name': Validation.name_validator, 'last_name': Validation.name_validator,
                         'email': Validation.email_validator, 'password': Validation.pass_validator}
        errors = {}
        password = False
        iteration_test = 0
        for c in request.args:
            iteration_test += 1
            if c == 'id':
                errors['id'] = 'cannot edit id'
            if c == 'access':
                errors['access'] = 'cannot change access level'
            if c not in args:
                errors[c] = 'no such parameter'
            else:
                validate = args_validate[c](request.args[c])
                if validate is not True:
                    errors[c] = validate
                else:
                    if c == 'password':
                        password = True
                    else:
                        data.append(request.args[c])
                        column.append(c)
        if not errors and iteration_test != 0:
            to_do = []
            for c in range(0, len(data)):
                to_do.append(str(column[c]) + ' = \'' + str(data[c]) + '\'')
            to_do = 'update users set ' + ', '.join(to_do) + ' where id = ' + str(g_id)
            cursor.execute(to_do)
            if password:
                key = hashlib.pbkdf2_hmac('sha256', str(request.args['password']).encode('utf-8'), salt, 100000)
                storage = salt + key
                query = 'update users set password = %s where id = \'' + str(g_id) + '\';'
                cursor.execute(query, (storage,))
            db.commit()
            return jsonify({'status': '200', 'message': 'successfully edited user'})
        elif iteration_test == 0:
            return jsonify({'status': '400', 'errors': 'need input parameters'})
        else:
            return jsonify({'status': '400', 'errors': errors})

    return jsonify({'status': '404', 'message': 'No such user'})


if __name__ == '__main__':

    db = MySQLdb.connect("localhost", "root", "Az27061985", "test")
    cursor = db.cursor()
    user_id = -1
    access_level = 'user'
    cursor.execute("Select* From events;")
    parameters = ['id', 'title', 'rest_name', 'date', 'time', 'duration', 'price', 'user_id', 'amount']
    collection = []
    iteration = 0
    for q in cursor:
        collection.append(dict())
        for z in range(0, len(parameters)):
            collection[iteration][parameters[z]] = str(q[z])
        iteration += 1
    all_events = Collection(collection)
    current_ord = []
    salt = os.urandom(32)
    hello.run()
    db.close()
