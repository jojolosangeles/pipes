import json

from model.entity.entity import EntityFactory
from pipes.rabbitmq import RabbitMQ
from timelines.entity_extractor import EntityExtractor


class PipelineProcessor:

    def __init__(self, input_queue_name, output_queue_name, output_router, line_processor):
        self.input_queue = RabbitMQ('localhost', input_queue_name, line_processor)
        output_router.set_output_queue(output_queue_name)

    def start(self):
        self.input_queue.receive()

class TimeLineEngine:
    def __init__(self):
        self.entityFactory = EntityFactory()
        self.entities = EntityExtractor(self.entityFactory)

    def set_output_queue(self, queue_name):
        print("Set output queue name to '{}'".format(queue_name))

    def process_line(self, line):
        #print("Line: {}".format(line))
        json_data = json.loads(line)
        self.entities.process_json(json_data)
        #print("json_data={}".format(json_data))

if __name__ == "__main__":
    timeline_engine = TimeLineEngine()
    pp = PipelineProcessor('jsonq', 'timeline', timeline_engine, timeline_engine.process_line)
    pp.start()