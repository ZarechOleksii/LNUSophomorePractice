from flask import Flask, jsonify, request
from Collection import Collection
from Event import Event


hello = Flask(__name__)
all_events = Collection('ToRead.json')
hello.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
hello.config['JSON_SORT_KEYS'] = False


@hello.route('/events', methods=['GET'])
def print_all_and_search():
    if 'what' in request.args:
        to_search = request.args['what']
        return jsonify(all_events.search3(to_search))
    elif 'sort_by' in request.args and 'sort_type' in request.args:
        to_return = all_events.sorting3(request.args['sort_by'], request.args['sort_type'])
        all_events.rewrite()
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
        all_events.append(new_event)
        all_events.rewrite()
        return jsonify({'status': '200', 'message': 'Successfully created'})


@hello.route('/events/<g_id>', methods=['DELETE'])
def deleting_one(g_id):
    if all_events.delete_id(g_id):
        all_events.rewrite()
        return jsonify({'status': '200', 'message': 'Successfully deleted'})
    else:
        return jsonify({'status': '404', 'message': 'No such ID'})


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
            all_events.rewrite()
        return jsonify(all_events.edit_entire_event(to_edit, request.args))
    else:
        return jsonify({'status': '404', 'message': 'No such ID'})


if __name__ == '__main__':
    hello.run()
