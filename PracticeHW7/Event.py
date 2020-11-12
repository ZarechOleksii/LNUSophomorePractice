from Observer import Observer


class Event:
    @staticmethod
    def to_do(key, to_print):
        for x in Observer.attachments:
            if x == key:
                Observer.attachments[x](to_print)
                break
