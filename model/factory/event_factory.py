from inspect import getmembers, isclass, isabstract
import model.events


class EventFactory:

    events = {}   # Key = event name, value = event class

    def __init__(self, abbreviations):
        self.load_events()
        self.abbreviations = abbreviations

    def load_events(self):
        concrete_classes = getmembers(model.events, lambda m: isclass(m) and not isabstract(m))
        for name, _type in concrete_classes:
            if (isclass(_type) and issubclass(_type, model.events.AbsEvent)):
                self.events.update([[_type.EVENT_NAME, _type]])

    def create_instance(self, name, json_data):
        if name in self.events:
            return self.events[name](json_data, self.abbreviations)
        else:
            return model.events.NullEvent(name)