import json

from model.entity.entity import EntityFactory
from timelines.entity_extractor import EntityExtractor
from timelines.timeline_extractor import TimelineExtractor


class Timeline(object):

    def __init__(self, entities, events):
        self.entities = [ entity.name for entity in entities ]
        self.events = events

    def toJSON(self):
        return '{{ "entities": {}, "timeline": [{}] }}'.format(
            json.dumps(self.entities), ", ".join([ e.toJSON() for e in self.events ]))

class TimelineEngine:
    def __init__(self, output_channels):
        self.output_channels = output_channels
        self.abbreviations = {}
        self.entityExtractor = EntityExtractor(EntityFactory(), self.abbreviations)
        self.timelineExtractor = TimelineExtractor(self.abbreviations)

    def __call__(self, line, *args, **kwargs):
        json_data = json.loads(line)
        self.entityExtractor(json_data)
        self.timelineExtractor(json_data)

    def terminate(self):
        """Build a JSON object to represent the timeline sequence.

        {
          "entities": [ ... comma separated list of entity names ... ],
          "timeline": [
              ... for each timeline entry ...
               event {
                 "from_entity_name": "...name...",
                 "to_entity_name": "...name...",
                 "start_time": "..t1..",
                 "end_time": "..t2..",
                 "message": "..whatever.."
               }, ..
            ]
        }"""

        result = Timeline(self.entityExtractor.entities, self.timelineExtractor.time_spanning_events)
        self.output_channels.send(result.toJSON())
