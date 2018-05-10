from model.factory.event_factory import EventFactory


class TimelineExtractor:
    """Creates synchronized timelines for each entity."""
    def __init__(self, abbreviations):
        self.time_spanning_events = []
        self.current_time = {}
        self.abbreviations = abbreviations
        self.event_factory = EventFactory(abbreviations)
        self.max_time = 0

    def __call__(self, json_data):
        command = json_data['command']
        event = self.event_factory.create_instance(command, json_data)
        if event.spans_time():
            self.time_spanning_events.append(event)
            event.set_time(self.current_time.get(event.from_entity, self.max_time))
            if event.end_time >= self.current_time.get(event.to_entity, event.end_time):
                self.current_time[event.to_entity] = event.end_time
        elif event.__class__.__name__ == "SyncEvent":
            self.max_time = max([self.current_time[e] for e in self.current_time.keys() if e in event.entities])
            for k in event.entities:
                self.current_time[k] = self.max_time
        return event
