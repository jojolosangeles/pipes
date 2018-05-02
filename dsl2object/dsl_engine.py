from dsl2object.entity_dsl import EntityDSL, EntityTimeDSL, EntityStateDSL
from dsl2object.message_dsl import MessageDSL
from pipes.rabbitmq import RabbitMQ

class QueueOutputStream:
    def __init__(self, queueName):
        self.queueName = queueName

    def write(self, s):
        rmq = RabbitMQ('localhost',self.queueName)
        rmq.send(s)

class DSL_Engine:
    def __init__(self, output_channels):
        self.entity_dsl = EntityDSL()
        self.entity_time_dsl = EntityTimeDSL()
        self.entity_state_dsl = EntityStateDSL()
        self.message_dsl = MessageDSL()
        self.current_line_number = 0
        self.processors = [ self.entity_dsl, self.entity_time_dsl, self.entity_state_dsl, self.message_dsl ]
        self.output_channels = output_channels

    def __call__(self, line, *args, **kwargs):
        self.process_line(line)

    def terminate(self):
        pass

    def process_line(self, line):
        line_id = self.current_line_number
        self.current_line_number += 1
        for processor in self.processors:
            processor.process_line(line, line_id, self.output_channels)

    def process_json(self, json_text):
        pass
