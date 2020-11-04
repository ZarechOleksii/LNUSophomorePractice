import unittest
from Collection import Collection
from Event import Event


class TestHW7(unittest.TestCase):
    test_dict = {'id': '1',
                 'duration': '1.2',
                 'price': '2.54',
                 'rest_name': '2',
                 'title': 'TestName',
                 'date': ['2020', '2', '22'],
                 'time': ['14', '30']}

    def test_file_name(self):
        self.assertTrue(Collection('ToRead.txt'), 'Fail file name (cannot happen)')

    def test_validation_id(self):
        self.assertEqual(Event(self.test_dict).id, 1, 'Failed to create object')
        self.test_dict['id'] = 'abc'
        self.assertNotEqual(Event(self.test_dict).id, 'abc', 'ID is not a number')
        self.test_dict['id'] = '-5'
        self.assertNotEqual(Event(self.test_dict).id, -5, 'ID is negative')

        self.test_dict['id'] = '1'
        self.assertEqual(Event(self.test_dict).id, 1, 'ID was not accepted')

    def test_validation_duration(self):
        self.test_dict['duration'] = 'abc'
        self.assertNotEqual(Event(self.test_dict).id, 1, 'Duration is not a number')
        self.test_dict['duration'] = '-3'
        self.assertNotEqual(Event(self.test_dict).id, 1, 'Duration is negative')

        self.test_dict['duration'] = '2'
        self.assertEqual(Event(self.test_dict).id, 1, 'Duration did not let initialization to happen')
        self.assertEqual(Event(self.test_dict).duration, 2, 'Duration is wrong')
        self.test_dict['duration'] = '2.421'
        self.assertEqual(Event(self.test_dict).id, 1, 'Duration did not let initialization to happen')
        self.assertNotEqual(Event(self.test_dict).duration, 2.421, 'Duration is wrong')
        self.assertEqual(Event(self.test_dict).duration, 2.4, 'Duration is wrong')

    def test_validation_price(self):
        self.test_dict['price'] = 'abc'
        self.assertNotEqual(Event(self.test_dict).id, 1, 'Price is not a number')
        self.test_dict['price'] = '-3'
        self.assertNotEqual(Event(self.test_dict).id, 1, 'Price is negative')

        self.test_dict['price'] = '2'
        self.assertEqual(Event(self.test_dict).id, 1, 'Price did not let initialization to happen')
        self.assertEqual(Event(self.test_dict).price, 2, 'Price is wrong')
        self.test_dict['price'] = '2.421'
        self.assertEqual(Event(self.test_dict).id, 1, 'Price did not let initialization to happen')
        self.assertNotEqual(Event(self.test_dict).price, 2.421, 'Price is wrong')
        self.assertEqual(Event(self.test_dict).price, 2.42, 'Price is wrong')

    def test_validation_restaurant(self):
        self.test_dict['rest_name'] = 'abc'
        self.assertNotEqual(Event(self.test_dict).id, 1, 'Restaurant name is not a number')
        self.test_dict['rest_name'] = '5'
        self.assertNotEqual(Event(self.test_dict).id, 1, 'Restaurant name is not in the list')

        self.test_dict['rest_name'] = '2'
        self.assertEqual(Event(self.test_dict).id, 1, 'Restaurant name was not accepted')

    def test_validation_title(self):
        self.test_dict['title'] = '-abc'
        self.assertNotEqual(Event(self.test_dict).id, 1, 'Title contains forbidden characters')
        self.test_dict['title'] = '|abc'
        self.assertNotEqual(Event(self.test_dict).id, 1, 'Title contains forbidden characters')
        self.test_dict['title'] = ':abc'
        self.assertNotEqual(Event(self.test_dict).id, 1, 'Title contains forbidden characters')

        self.test_dict['title'] = 'abc'
        self.assertEqual(Event(self.test_dict).id, 1, 'Title was not accepted')

    def test_validation_date(self):
        self.test_dict['date'] = ['20a0', '2', '22']
        self.assertNotEqual(Event(self.test_dict).id, 1, 'Year contains letters')
        self.test_dict['date'] = ['2020', 'a', '22']
        self.assertNotEqual(Event(self.test_dict).id, 1, 'Month contains letters')
        self.test_dict['date'] = ['2020', '2', 'a']
        self.assertNotEqual(Event(self.test_dict).id, 1, 'Day contains letters')
        self.test_dict['date'] = ['2020', '2', '30']
        self.assertNotEqual(Event(self.test_dict).id, 1, 'Day out of range')
        self.test_dict['date'] = ['2019', '2', '29']
        self.assertNotEqual(Event(self.test_dict).id, 1, 'Day out of range')
        self.test_dict['date'] = ['2019', '15', '15']
        self.assertNotEqual(Event(self.test_dict).id, 1, 'Month out of range')

        self.test_dict['date'] = ['2020', '2', '28']
        self.assertEqual(Event(self.test_dict).id, 1, 'Date was not accepted')

    def test_validation_time(self):
        self.test_dict['time'] = ['1a', '59']
        self.assertNotEqual(Event(self.test_dict).id, 1, 'Hour contains letters')
        self.test_dict['time'] = ['14', '5a']
        self.assertNotEqual(Event(self.test_dict).id, 1, 'Minute contains letters')
        self.test_dict['time'] = ['14', '60']
        self.assertNotEqual(Event(self.test_dict).id, 1, 'Minute out of range')
        self.test_dict['time'] = ['24', '00']
        self.assertNotEqual(Event(self.test_dict).id, 1, 'Hour out of range')

        self.test_dict['time'] = ['14', '30']
        self.assertEqual(Event(self.test_dict).id, 1, 'Time was not accepted')

    def test_collection_basic(self):
        test_dict = {'id': '1',
                     'duration': '1.2',
                     'price': '2.54',
                     'rest_name': '2',
                     'title': 'TestName',
                     'date': ['2020', '2', '22'],
                     'time': ['14', '30']}
        test_event1 = Event(test_dict)
        test_dict['id'] = '2'
        test_event2 = Event(test_dict)
        test_collection = Collection('Tests/EmptyFile.txt')
        #   append, len and getitem test
        self.assertEqual(len(test_collection), 0, 'Wrong length')
        test_collection.append(test_event1)
        self.assertEqual(len(test_collection), 1, 'Wrong length')
        test_collection.append(test_event2)
        self.assertEqual(len(test_collection), 2, 'Wrong length')
        self.assertIs(test_collection[0], test_event1, 'Wrong object')
        self.assertIs(test_collection[1], test_event2, 'Wrong object')
        #   deletion test
        self.assertFalse(test_collection.delete_id('Wrong input'), 'Has to be false')
        self.assertFalse(test_collection.delete_id(57), 'Has to be false')
        self.assertTrue(test_collection.delete_id(1), 'Has to be true')
        self.assertEqual(len(test_collection), 1, 'Wrong length')
        self.assertIs(test_collection[0], test_event2, 'Wrong object')
        #   editing element test
        self.assertFalse(test_collection.edit_one(test_collection.find_by_id(2), 'title', '-abc'), 'Should not edit')
        self.assertTrue(test_collection.edit_one(test_collection.find_by_id(2), 'title', 'good name'), 'Should edit')

    def test_collection_sort_write(self):
        test_collection = Collection('Tests/SortTest.txt')

        #   testing sorting by title
        test_collection.sorting2('T')
        test_collection.rewrite()
        manual_file = open('Tests/ByTitle.txt', 'r')
        manually_sorted = manual_file.read()
        manual_file.close()
        program_file = open('Tests/SortTest.txt')
        program_sorted = program_file.read()
        program_file.close()
        self.assertEqual(manually_sorted, program_sorted, 'Wrong title sort')

        #   testing sorting by id
        test_collection.sorting2('I')
        test_collection.rewrite()
        manual_file = open('Tests/ByID.txt', 'r')
        manually_sorted = manual_file.read()
        manual_file.close()
        program_file = open('Tests/SortTest.txt')
        program_sorted = program_file.read()
        program_file.close()
        self.assertEqual(manually_sorted, program_sorted, 'Wrong id sort')

        #   testing sorting by restaurant names
        test_collection.sorting2('R')
        test_collection.rewrite()
        manual_file = open('Tests/ByRestaurantName.txt', 'r')
        manually_sorted = manual_file.read()
        manual_file.close()
        program_file = open('Tests/SortTest.txt')
        program_sorted = program_file.read()
        program_file.close()
        self.assertEqual(manually_sorted, program_sorted, 'Wrong restaurant names sort')

        #   testing sorting by date
        test_collection.sorting2('Da')
        test_collection.rewrite()
        manual_file = open('Tests/ByDate.txt', 'r')
        manually_sorted = manual_file.read()
        manual_file.close()
        program_file = open('Tests/SortTest.txt')
        program_sorted = program_file.read()
        program_file.close()
        self.assertEqual(manually_sorted, program_sorted, 'Wrong date sort')

        #   testing sorting by time
        test_collection.sorting2('Ti')
        test_collection.rewrite()
        manual_file = open('Tests/ByTime.txt', 'r')
        manually_sorted = manual_file.read()
        manual_file.close()
        program_file = open('Tests/SortTest.txt')
        program_sorted = program_file.read()
        program_file.close()
        self.assertEqual(manually_sorted, program_sorted, 'Wrong time sort')

        #   testing sorting by duration
        test_collection.sorting2('D')
        test_collection.rewrite()
        manual_file = open('Tests/ByDuration.txt', 'r')
        manually_sorted = manual_file.read()
        manual_file.close()
        program_file = open('Tests/SortTest.txt')
        program_sorted = program_file.read()
        program_file.close()
        self.assertEqual(manually_sorted, program_sorted, 'Wrong duration sort')

        #   testing sorting by price
        test_collection.sorting2('P')
        test_collection.rewrite()
        manual_file = open('Tests/ByPrice.txt', 'r')
        manually_sorted = manual_file.read()
        manual_file.close()
        program_file = open('Tests/SortTest.txt')
        program_sorted = program_file.read()
        program_file.close()
        self.assertEqual(manually_sorted, program_sorted, 'Wrong price sort')

        test_collection.sorting2('I')
        test_collection.rewrite()

    def test_collection_searching(self):
        test_collection = Collection('Tests/SearchTest.txt')

        self.assertEqual(test_collection.search2('NotExists'), '', 'Should not find anything')

        self.assertEqual(test_collection.search2(''), '', 'Should not find anything')

        to_find = 'Event with ID 10 has ID 10\nEvent with ID 5 has price 10.5\n'
        self.assertEqual(test_collection.search2('10'), to_find, 'Should find same')

        to_find = 'Event with ID 5 has title FourthEvent\nEvent with ID 10 has title firstEvent\n'
        self.assertEqual(test_collection.search2('Event'), to_find, 'Should find same')

        to_find = 'Event with ID 1 has starting date 2019-05-25\n'
        to_find += 'Event with ID 5 has starting date 2005-11-22\n'
        to_find += 'Event with ID 10 has starting date 2021-12-31\n'
        self.assertEqual(test_collection.search2('20'), to_find, 'Should find same')

    def test_history(self):
        test_dict = {'id': '1',
                     'duration': '1.2',
                     'price': '2.54',
                     'rest_name': '2',
                     'title': 'TestName',
                     'date': ['2020', '2', '22'],
                     'time': ['14', '30']}
        test_collection = Collection('TestsHistory/ChangingFile.txt')

        test_collection.delete_id(4)
        test_collection.rewrite()
        manual_file = open('TestsHistory/Action1.txt', 'r')
        manual_action = manual_file.read()
        manual_file.close()
        program_file = open('TestsHistory/ChangingFile.txt')
        program_action = program_file.read()
        program_file.close()
        self.assertEqual(manual_action, program_action)

        test_collection.delete_id(1)
        test_collection.rewrite()
        manual_file = open('TestsHistory/Action2.txt', 'r')
        manual_action = manual_file.read()
        manual_file.close()
        program_file = open('TestsHistory/ChangingFile.txt')
        program_action = program_file.read()
        program_file.close()
        self.assertEqual(manual_action, program_action)

        test_collection.append(Event(test_dict))
        test_collection.rewrite()
        manual_file = open('TestsHistory/Action3.txt', 'r')
        manual_action = manual_file.read()
        manual_file.close()
        program_file = open('TestsHistory/ChangingFile.txt')
        program_action = program_file.read()
        program_file.close()
        self.assertEqual(manual_action, program_action)

        test_collection.delete_id(14)
        test_collection.rewrite()
        manual_file = open('TestsHistory/Action4.txt', 'r')
        manual_action = manual_file.read()
        manual_file.close()
        program_file = open('TestsHistory/ChangingFile.txt')
        program_action = program_file.read()
        program_file.close()
        self.assertEqual(manual_action, program_action)

        # going back in history
        test_collection.undo()
        test_collection.rewrite()
        manual_file = open('TestsHistory/Action3.txt', 'r')
        manual_action = manual_file.read()
        manual_file.close()
        program_file = open('TestsHistory/ChangingFile.txt')
        program_action = program_file.read()
        program_file.close()
        self.assertEqual(manual_action, program_action)

        test_collection.undo()
        test_collection.rewrite()
        manual_file = open('TestsHistory/Action2.txt', 'r')
        manual_action = manual_file.read()
        manual_file.close()
        program_file = open('TestsHistory/ChangingFile.txt')
        program_action = program_file.read()
        program_file.close()
        self.assertEqual(manual_action, program_action)

        test_collection.undo()
        test_collection.rewrite()
        manual_file = open('TestsHistory/Action1.txt', 'r')
        manual_action = manual_file.read()
        manual_file.close()
        program_file = open('TestsHistory/ChangingFile.txt')
        program_action = program_file.read()
        program_file.close()
        self.assertEqual(manual_action, program_action)

        #   going forward in history
        test_collection.redo()
        test_collection.rewrite()
        manual_file = open('TestsHistory/Action2.txt', 'r')
        manual_action = manual_file.read()
        manual_file.close()
        program_file = open('TestsHistory/ChangingFile.txt')
        program_action = program_file.read()
        program_file.close()
        self.assertEqual(manual_action, program_action)

        test_collection.redo()
        test_collection.rewrite()
        manual_file = open('TestsHistory/Action3.txt', 'r')
        manual_action = manual_file.read()
        manual_file.close()
        program_file = open('TestsHistory/ChangingFile.txt')
        program_action = program_file.read()
        program_file.close()
        self.assertEqual(manual_action, program_action)

        #   going back again
        test_collection.undo()
        test_collection.rewrite()
        manual_file = open('TestsHistory/Action2.txt', 'r')
        manual_action = manual_file.read()
        manual_file.close()
        program_file = open('TestsHistory/ChangingFile.txt')
        program_action = program_file.read()
        program_file.close()
        self.assertEqual(manual_action, program_action)

        #   changing history in some place
        test_collection.delete_id(8)
        test_collection.rewrite()
        manual_file = open('TestsHistory/Action3Alternative.txt', 'r')
        manual_action = manual_file.read()
        manual_file.close()
        program_file = open('TestsHistory/ChangingFile.txt')
        program_action = program_file.read()
        program_file.close()
        self.assertEqual(manual_action, program_action)

        #   trying to redo after undoing and then doing another action
        test_collection.redo()
        test_collection.rewrite()
        manual_file = open('TestsHistory/Action3Alternative.txt', 'r')
        manual_action = manual_file.read()
        manual_file.close()
        program_file = open('TestsHistory/ChangingFile.txt')
        program_action = program_file.read()
        program_file.close()
        self.assertEqual(manual_action, program_action)

        #   going back to start
        test_collection.undo()
        test_collection.rewrite()
        manual_file = open('TestsHistory/Action2.txt', 'r')
        manual_action = manual_file.read()
        manual_file.close()
        program_file = open('TestsHistory/ChangingFile.txt')
        program_action = program_file.read()
        program_file.close()
        self.assertEqual(manual_action, program_action)

        test_collection.undo()
        test_collection.rewrite()
        manual_file = open('TestsHistory/Action1.txt', 'r')
        manual_action = manual_file.read()
        manual_file.close()
        program_file = open('TestsHistory/ChangingFile.txt')
        program_action = program_file.read()
        program_file.close()
        self.assertEqual(manual_action, program_action)

        test_collection.undo()
        test_collection.rewrite()
        manual_file = open('TestsHistory/Start.txt', 'r')
        manual_action = manual_file.read()
        manual_file.close()
        program_file = open('TestsHistory/ChangingFile.txt')
        program_action = program_file.read()
        program_file.close()
        self.assertEqual(manual_action, program_action)

        #   trying to undo when there is nothing to undo
        test_collection.undo()
        test_collection.rewrite()
        manual_file = open('TestsHistory/Start.txt', 'r')
        manual_action = manual_file.read()
        manual_file.close()
        program_file = open('TestsHistory/ChangingFile.txt')
        program_action = program_file.read()
        program_file.close()
        self.assertEqual(manual_action, program_action)


if __name__ == '__main__':
    unittest.main()
