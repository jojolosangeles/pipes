import json

class TimeSpanningEvent:
    """Contains an event that spans a time window, within a single entity
    as a 'state', or between two entities as a 'message'."""
    def __init__(self, from_entity, to_entity, start_time, end_time, message):
        self.from_entity = from_entity
        self.to_entity = to_entity
        self.start_time = start_time
        self.end_time = end_time
        self.message = message

    def toJSON(self):
        return '{{ "from_entity": "{}", "to_entity": "{}", "start_time": "{}", "end_time": "{}", "message": "{}" }}'\
            .format(self.from_entity, self.to_entity, self.start_time, self.end_time, self.message)

    def __repr__(self):
        return "t{}:{} '{}' t{}:{}\n".format(self.start_time, self.from_entity.name, self.message, self.end_time, self.to_entity.name)

class TimelineExtractor:
    """Creates synchronized timelines for each entity."""
    SEND_MESSAGE = "send_message"
    FROM = "from_entity"
    TO = "to_entity"
    DELAY = "delay"

    SET_STATE = "set_state"
    ENTITY_NAME = "name"

    def __init__(self, abbreviations):
        self.time_spanning_events = []
        self.current_time = {}
        self.abbreviations = abbreviations

    def __call__(self, json_data, *args, **kwargs):
        command = json_data['command']

        if command == self.SEND_MESSAGE:
            from_entity = self.expand(json_data[self.FROM])
            to_entity = self.expand(json_data[self.TO])
            start_time = self.current_time.get(from_entity, 0)
            end_time = start_time + int(json_data[self.DELAY])
            message = json_data['message']
            self.time_spanning_events.append(
                TimeSpanningEvent(from_entity, to_entity, start_time, end_time, message)
            )
            self.current_time[to_entity] = end_time
        elif command == self.SET_STATE:
            from_entity = to_entity = self.expand(json_data[self.ENTITY_NAME])
            start_time = self.current_time.get(from_entity, 0)
            end_time = start_time + int(json_data[self.DELAY])
            message = json_data['state']
            self.time_spanning_events.append(
                TimeSpanningEvent(from_entity, to_entity, start_time, end_time, message)
            )

    def expand(self, entity):
        if len(entity) < 3:
            entity = self.abbreviations[entity]
        return entity

    def get_time_spanning_events(self, entity):
        try:
            return self.time_spanning_events[entity]
        except:
            return 0