import MySQLdb
from Collection import Collection
from flask import Flask, jsonify, request
from Event import Event

hello = Flask(__name__)
hello.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
hello.config['JSON_SORT_KEYS'] = False


def update(events):
    data = events.rewrite()
    cursor.execute("DELETE FROM Events;")
    db.commit()
    for x in data:
        cursor.execute("INSERT INTO events VALUES " + str(x) + ';')
    db.commit()


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
    return jsonify(to_return)


@hello.route('/events/<g_id>', methods=['GET'])
def print_one(g_id):
    to_return = all_events.find_by_id(g_id)
    if to_return is not False:
        to_return = to_return.to_write()
    else:
        return jsonify({'status': '404', 'message': 'No such ID'})
    return jsonify(to_return)


@hello.route('/events/<g_id>', methods=['DELETE'])
def deleting_one(g_id):
    if all_events.delete_id(g_id):
        cursor.execute("DELETE FROM Events WHERE id = " + str(g_id) + ";")
        db.commit()
        return jsonify({'status': '200', 'message': 'Successfully deleted'})
    else:
        return jsonify({'status': '404', 'message': 'No such ID'})


@hello.route('/events', methods=['POST'])
def add_one():
    param_set = ('id', 'duration', 'price', 'rest_name', 'title', 'date', 'time')
    to_give = dict()
    for x in param_set:
        if x not in request.args:
            return jsonify({'status': '400', 'message': 'Missing parameters'})
        else:
            to_give[x] = request.args[x]
    new_event = Event(to_give)
    if new_event.id == -1:
        return jsonify({'status': '400', 'message': 'wrong input', 'errors': new_event.errors})
    else:
        to_return = all_events.append(new_event)
        if to_return['status'] == '200':
            data = (to_give['id'], to_give['title'], to_give['rest_name'], to_give['date'], to_give['time'],
                    to_give['duration'], to_give['price'])
            to_do = """INSERT INTO events 
                    VALUES""" + str(data) + ';'
            cursor.execute(to_do)
            db.commit()
        return jsonify(to_return)


@hello.route('/events/<g_id>', methods=['PUT'])
def edit_one(g_id):
    to_edit = all_events.find_by_id(g_id)
    if to_edit is not False:
        current = to_edit.to_write()
        for x in request.args:
            if x not in current:
                return jsonify({'status': '400', 'message': 'No such parameter'})
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

    cursor.execute("Select* From Events;")

    parameters = ['id', 'title', 'rest_name', 'date', 'time', 'duration', 'price']
    test = []
    iteration = 0
    for q in cursor:
        test.append(dict())
        for z in range(0, len(parameters)):
            test[iteration][parameters[z]] = str(q[z])
        iteration += 1
    all_events = Collection(test)
    hello.run()
    db.close()
