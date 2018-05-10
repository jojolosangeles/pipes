from model.events.abstract_event import AbsEvent

class SyncEvent(AbsEvent):
    EVENT_NAME = "sync"
    ENTITIES = "entities"

    def __init__(self, json_data, abbreviations):
        self.entities = [abbreviations.get(e,e) for e in json_data[self.ENTITIES].split(",")]

    def toJSON(self):
        return '{ "sync": "*" }'

