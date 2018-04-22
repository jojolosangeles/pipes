from dsl2object.entity_dsl import EntityDSL, EntityTimeDSL, EntityStateDSL
from dsl2object.message_dsl import MessageDSL
import sys

from pipes.rabbitmq import RabbitMQ


class FakeOutputStream:
    def __init__(self):
        pass

    @classmethod
    def write(self, s):
        sys.stdout.write(s)

class QueueOutputStream:
    def __init__(self, queueName):
        self.queueName = queueName

    def write(self, s):
        rmq = RabbitMQ('localhost',self.queueName)
        rmq.send(s)
        #sys.stdout.write("Put in queue '{}': '{}'".format(self.queueName, s))


class DSL_Engine:
    def __init__(self, output_channel):
        self.entity_dsl = EntityDSL()
        self.entity_time_dsl = EntityTimeDSL()
        self.entity_state_dsl = EntityStateDSL()
        self.message_dsl = MessageDSL()
        self.current_line_number = 0
        self.processors = [ self.entity_dsl, self.entity_time_dsl, self.entity_state_dsl, self.message_dsl ]
        self.output_channel = output_channel

    def __call__(self, line, *args, **kwargs):
        self.process_line(line)

    def process_line(self, line):
        line_id = self.current_line_number
        self.current_line_number += 1
        for processor in self.processors:
            processor.process_line(line, line_id, self.output_channel)

    def process_json(self, json_text):
        pass
