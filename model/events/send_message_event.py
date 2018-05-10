from model.events.time_spanning_event import TimeSpanningEvent

class SendMessageEvent(TimeSpanningEvent):
    """Contains an event that spans a time window, within a single entity
    as a 'state', or between two entities as a 'message'."""
    EVENT_NAME = "send_message"

    MESSAGE = "message"
    FROM = "from_entity"
    TO = "to_entity"
    DELAY = "delay"

    def __init__(self, json_data, abbreviations):
        from_entity = abbreviations.get(json_data[self.FROM], json_data[self.FROM])
        to_entity = abbreviations.get(json_data[self.TO], json_data[self.TO])
        delay = int(json_data[self.DELAY])
        message = json_data[self.MESSAGE]
        super().__init__(from_entity, to_entity, delay, message)