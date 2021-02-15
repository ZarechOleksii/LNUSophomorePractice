import copy


class Momento:
    def __init__(self, given):
        self.all_events_momento = copy.deepcopy(given)

    def get_momento_value(self):
        return self.all_events_momento
