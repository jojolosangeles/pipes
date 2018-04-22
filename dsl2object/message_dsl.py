from dsl2object.base_processor import BaseProcessor
from dsl2object.events import MessageEvent
import json
import re

class MessageDSL(BaseProcessor):
    """Handles the part of the DSL that creates messages."""
    def __init__(self):
        super()
        self.last_message_received = {}  # "*" for message uses value from here

    def process(self, data, originating_event_id, output_channel):
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
                output_channel.send(json.dumps(vars(message_event)))
        except:
            pass

    def process_line(self, line, originating_event_id, output_channel):
        data = line.split()
        if len(data) >= 3 and data[1][0] == '(':
            self.process(data, originating_event_id, output_channel)
