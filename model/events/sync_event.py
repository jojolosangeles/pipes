from model.events.abstract_event import AbsEvent

class SyncEvent(AbsEvent):
    ENTITIES = "entities"
    EVENT_NAME = "sync"

    def __init__(self, json_data, abbreviations):
        self.entities = [abbreviations.get(e,e) for e in json_data[self.ENTITIES].split(",")]

    def toJSON(self):
        return '{ "{}": "*" }'.format(self.EVENT_NAME)

