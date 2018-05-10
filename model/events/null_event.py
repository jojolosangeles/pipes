from model.events.abstract_event import AbsEvent

class NullEvent(AbsEvent):
    EVENT_NAME = "null"

    def __init__(self, name):
        self.name = name

    def set_time(self, start_time):
        print("HEY WTF, NullEvent getting a set_time call: {}".format(self.name))

