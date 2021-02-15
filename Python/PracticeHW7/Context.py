from Validation import Validation


class Context:
    def __init__(self):
        self.strategy = None

    def set_strategy(self, g_strategy):
        self.strategy = g_strategy

    def get_strategy(self):
        return self.strategy

    @Validation.decorator_context
    def generate(self, l_list, pos, given):
        if self.strategy is not None:
            return self.strategy.generate(l_list, pos, given)
        else:
            print('No strategy chosen')
            return False
