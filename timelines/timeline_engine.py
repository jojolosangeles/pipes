import json

from model.entity.entity import EntityFactory
from timelines.entity_extractor import EntityExtractor

class TimeLineEngine:
    def __init__(self):
        self.entityExtractor = EntityExtractor(EntityFactory())

    def process_line(self, line):
        json_data = json.load(line)
        self.entityExtractor(json_data)