import json
import re

from dsl2object.base_processor import BaseProcessor, skip_empty_lines
from dsl2object.events import MessageEvent

class MessageDSL(BaseProcessor):
    """Handles the part of the DSL that creates messages."""
    def __init__(self):
        super()
        self.last_message_received = {}  # "*" for message uses value from here

    def process(self, data, originating_event_id, output_channels):
        """Convert a list of tokens into a list of instances.
        Syntax we are looking for:

        <entity 1> (transit_time)<message> <entity 2>

        NodeA (3)x=3 NodeB
        """

        s = re.search( r'\((\d+)\)(.*)', data[1], re.M|re.I)
        try:
            delay = int(s.group(1))
            message = s.group(2)
            if len(data) > 3:
                message = ' '.join([message, *data[2:-1]])
            if message == "*":
                message = self.last_message_received[data[0]]
            for dest in data[-1].split(","):
                message_event = MessageEvent(data[0], delay, message, dest, originating_event_id)
                self.last_message_received[dest] = message
                output_channels.send(json.dumps(vars(message_event)))
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    @skip_empty_lines
    def process_line(self, line, originating_event_id, output_channels):
        data = line.split()
        if len(data) >= 3 and data[1][0] == '(':
            self.process(data, originating_event_id, output_channels)
