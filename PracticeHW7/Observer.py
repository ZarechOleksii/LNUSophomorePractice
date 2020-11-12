
class Observer:
    attachments = dict()

    @staticmethod
    def attach(key, method):
        Observer.attachments[key] = method
