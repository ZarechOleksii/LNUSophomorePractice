
class Event:

    amount = 1

    def __init__(self, g_title, g_rest, g_date_and_time, g_duration, g_price):
        self.id = Event.amount
        self.title = g_title
        self.rest_name = g_rest
        self.date_time = g_date_and_time
        self.duration = g_duration
        self.price = str(g_price) + ' $'
        Event.amount += 1

    def __str__(self):
        to_return = 'ID: ' + str(self.id) + '\n'
        to_return += 'Title: ' + self.title + '\n'
        to_return += 'Restaurant name: ' + self.rest_name.name + '\n'
        to_return += 'Date: ' + self.date_time.strftime("%x") + '\n'
        to_return += 'Time: ' + self.date_time.strftime("%X") + '\n'
        to_return += 'Duration: ' + str(self.duration) + ' hours' + '\n'
        to_return += 'Price: ' + self.price
        return to_return
