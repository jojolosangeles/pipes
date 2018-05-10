from model.events.abstract_event import AbsEvent

class TimeSpanningEvent(AbsEvent):
    """Contains an event that spans a time window, within a single entity
    as a 'state', or between two entities as a 'message'."""
    def __init__(self, from_entity, to_entity, delay, message):
        self.from_entity = from_entity
        self.to_entity = to_entity
        self.delay = delay
        self.message = message

    def spans_time(self):
        return True

    def set_time(self, start_time):
        self.start_time = start_time
        self.end_time = start_time + self.delay

    def toJSON(self):
        return '{{ "from_entity": "{}", "to_entity": "{}", "start_time": "{}", "end_time": "{}", "message": "{}" }}'\
            .format(self.from_entity, self.to_entity, self.start_time, self.end_time, self.message)

    def __repr__(self):
        return "t{}:{} '{}' t{}:{}\n".format(self.start_time, self.from_entity.name, self.message, self.end_time, self.to_entity.name)
