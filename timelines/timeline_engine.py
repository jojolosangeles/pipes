import json

from model.entity.entity import EntityFactory
from timelines.entity_extractor import EntityExtractor
from timelines.timeline_extractor import TimelineExtractor

class TimelineEngine:
    def __init__(self, output_channels):
        self.output_channels = output_channels
        self.abbreviations = {}
        self.entityExtractor = EntityExtractor(EntityFactory(), self.abbreviations)
        self.timelineExtractor = TimelineExtractor(self.abbreviations)

    def __call__(self, line, *args, **kwargs):
        json_data = json.loads(line)
        print(json_data)
        self.entityExtractor(json_data)
        print("ENTITIES={}".format(self.entityExtractor.entities))
        self.timelineExtractor(json_data)
        print("TIMELINE={}\n".format(self.timelineExtractor.latest_entity_time))

    def terminate(self):
        print(self.entityExtractor.entities)
        print(self.timelineExtractor.latest_entity_time)