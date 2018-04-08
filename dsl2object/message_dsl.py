from dsl2object.base_processor import BaseProcessor
from dsl2object.events import MessageEvent
import json
import re

class MessageDSL(BaseProcessor):
    """Handles the part of the DSL that creates messages."""
    def __init__(self):
        super()
        self.last_message_received = {}  # "*" for message uses value from here

    def process(self, data):
        """Convert a list of tokens into a list of instances.
        Syntax we are looking for:

        <entity 1> (transit_time)<message>-> <entity 2>

        NodeA (3)x=3 NodeB
        """

        s = re.search( r'\((\d+)\)(.*)', data[1], re.M|re.I)
        try:
            print("HERE")
            delay = int(s.group(1))
            print("B")
            message = s.group(2)
            print("C")
            if message == "*":
                print("D")
                message = self.last_message_received[data[0]]
            for dest in data[2].split(","):
                message_event = MessageEvent(data[0], delay, message, dest)
                self.last_message_received[dest] = message
                print("G")
                print("{}_to_{}".format(data[0], dest))
                print("G2")
                self.monitor_event(message_event, "{}_to_{}".format(data[0], dest))
                print("H")
                self.output_stream.write(json.dumps(vars(message_event)))
                print("I")
        except:
            print("WTF, got an exception!!!")
            pass

    def process_line(self, line):
        data = line.split()
        if len(data) == 3:
            self.process(data)
