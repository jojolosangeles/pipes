from model.events.time_spanning_event import TimeSpanningEvent

class SetStateEvent(TimeSpanningEvent):
    """Contains an event that spans a time window, within a single entity
    as a 'state', or between two entities as a 'message'."""
    EVENT_NAME = "set_state"

    ENTITY_NAME = "name"
    STATE = "state"
    DELAY = "delay"

    def __init__(self, json_data, abbreviations):
        entity_name = abbreviations.get(json_data[self.ENTITY_NAME], json_data[self.ENTITY_NAME])
        delay = int(json_data[self.DELAY]) - 1
        message = json_data[self.STATE]
        super().__init__(entity_name, entity_name, delay, message)
