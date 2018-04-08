import json
import time

from dsl2object.base_processor import EchoProcessor
from dsl2object.entity_dsl import EntityDSL, EntityTimeDSL
from dsl2object.message_dsl import MessageDSL

"""Distributed system communication simulation, using event sourcing and monitoring.
The monitor data is usable by visualization systems like kibana or honeycomb.
The DSL generates a sequence of events, which are then processed to create the visualiztion.

The DSL generated events:

DSL: entities Cluster 1/3, Node A, Person X, Bob, Player 1/11
(One line generates many events)
Entity event:
- id: <unique id for this event>
  type: create_entity
  name: <name>

DSL: <from entity name> (T)<message> <to entity name>
Time T is required, entity name can be any combination of characters in the name
with same order that uniquely identify the entity, e.g. "Player 1" can be abbreviated "P1"
Message event:
- id: <unique id for this event>
  type: send_message
  from_entity: <entity name>
  message: <message>
  to_enttiy: <entity name>

The Monitoring events (one type):
type: 'sent' or 'received'
trace: <originating event ID> so we can trace an event through system
sender: <sender ID>
channel: <channel ID>
event: <event ID>
time: <sent time>
"""

class LineProcessor:
    """Process all events, generate monitoring events.
    """
    def __init__(self, input_stream, output_stream, monitor_stream):
        self.input_stream = input_stream
        self.output_stream = output_stream
        self.monitor_stream = monitor_stream
        self.processors = []

    def register(self, processor):
        processor.set_streams(self.output_stream, self.monitor_stream)
        self.processors.append(processor)

    def run(self):
        for line in self.input_stream.stream:
            for processor in self.processors:
                processor.process_line(line)

class MonitorEvent:
    """Container for monitoring data.
    The Monitoring events (one type):
        type: 'sent' or 'received'
        trace: <originating event ID> so we can trace an event through system
        sender: <sender ID>
        channel: <channel ID>
        event: <event ID>
        time: <sent time>
        """

    SENT = 'sent'
    RECEIVED = 'received'
    idgen = 0

    TEXT_SENDER = 'text'

    @classmethod
    def genId(cls):
        cls.idgen += 1
        return cls.idgen

    def __init__(self, type, senderId, eventId, outputChannelId, msTime, traceId):
        self.type = type
        self.traceId = traceId
        self.outputChannelId = outputChannelId
        self.eventId = eventId
        self.msTime = msTime

class MonitoredStream:
    """Uniquely identified stream."""
    def __init__(self, stream, id):
        self.stream = stream
        self.id = id

    def write(self, s):
        self.stream.write(s)
        self.stream.write("\n")

    def monitor_send(self, line, output_stream_id):
        eventId = MonitorEvent.genId()
        event = MonitorEvent(MonitorEvent.SENT, MonitorEvent.TEXT_SENDER, eventId,
                             output_stream_id, round(time.time()*1000), eventId)
        self.write(json.dumps(vars(event)))

    def monitor_event(self, event, sender_id, output_stream_id):
        eventId = MonitorEvent.genId()
        event = MonitorEvent(MonitorEvent.SENT, sender_id, eventId,
                             output_stream_id, round(time.time()*1000), eventId)
        self.write(json.dumps(vars(event)))

INPUT_FILE_NAME = "data/ddia.figure8-3"  #"ddbsim.txt"
OUTPUT_FILE_NAME = "ddbsim_out.txt"
MONITOR_FILE_NAME = "ddbsim_monitor.txt"

entity_dsl = EntityDSL()
entity_time_dsl = EntityTimeDSL()
message_dsl = MessageDSL()
echoer = EchoProcessor()

with open(INPUT_FILE_NAME) as input_stream:
    input = MonitoredStream(input_stream, INPUT_FILE_NAME)
    with open(OUTPUT_FILE_NAME, "w") as output_stream:
        output = MonitoredStream(output_stream, OUTPUT_FILE_NAME)
        with open(MONITOR_FILE_NAME, "w") as monitor_stream:
            monitor = MonitoredStream(monitor_stream, MONITOR_FILE_NAME)
            line_processor = LineProcessor(input, output, monitor)
            line_processor.register(echoer)
            line_processor.register(entity_dsl)
            line_processor.register(entity_time_dsl)
            line_processor.register(message_dsl)
            line_processor.run()
