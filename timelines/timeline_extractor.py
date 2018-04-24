
class TimelineExtractor:
    """Creates synchronized timelines for each entity."""
    SEND_MESSAGE = "send_message"
    FROM = "from_entity"
    TO = "to_entity"
    DELAY = "delay"

    def __init__(self, abbreviations):
        self.universal_time = 0
        self.latest_entity_time = {}
        self.abbreviations = abbreviations

    def __call__(self, json_data, *args, **kwargs):
        if json_data['command'] == self.SEND_MESSAGE:
            self.record_time(json_data[self.FROM]),
            self.record_time(json_data[self.TO], json_data[self.DELAY])

    def record_time(self, entity, delay=0):
        if len(entity) < 3:
            entity = self.abbreviations[entity]
        entity_time = self.get_latest_entity_time(entity) + delay
        print("Record_time: {}, {}".format(entity, entity_time))
        self.latest_entity_time[entity] = entity_time

    def get_latest_entity_time(self, entity):
        try:
            return self.latest_entity_time[entity]
        except:
            return 0