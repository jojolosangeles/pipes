from dsl2object.base_processor import BaseProcessor
from dsl2object.events import FloatEvent, EntityEvent, StateEvent
from dsl2object.instance import InstanceFactory
import json
import itertools
import re

def is_not_digit(s):
    try:
        return not str.isdigit(s)
    except:
        return True

class EntityStateDSL(BaseProcessor):
    def process_line(self, line, line_id, output_channels):
        data = line.split()
        if len(data) >= 2:
            s = re.search( r'\((\d+)\)(.*)', data[0], re.M|re.I)
            try:
                delay = int(s.group(1))
                entity = s.group(2)
                state = ' '.join(data[1:])
                stateEvent = StateEvent(entity, state, delay, line_id)
                output_channels.send(json.dumps(vars(stateEvent)))
            except:
                pass

class EntityTimeDSL(BaseProcessor):
    """Set the time for an entity, input line are like this:  "N1.T=42.003"
    'N1' is an abbreviation for any entity.
    '.A=B' means that we add a key-value pair, keyValue['A'] = 'B'

    So for 'N1.float3.T=42.003' we need a 'set_float' event:

    """
    def process(self, data, originating_event_id, output_channels):
        """Process data array containing[ name, type, precision, value ]."""
        float_event = FloatEvent(data[0], data[1], data[2], data[3], originating_event_id)
        output_channels.send(json.dumps(vars(float_event)))

    def process_line(self, line, line_id, output_channels):
        data = line.split("=")
        if len(data) == 2:
            ntv = data[0].split(".")
            if len(ntv) == 3:
                data_type = "".join(itertools.takewhile(is_not_digit, ntv[1]))
                precision = ntv[1][len(data_type):]
                self.process(["{}.{}".format(ntv[0], ntv[2]), data_type, precision, data[1]], line_id, output_channels)


class EntityDSL(BaseProcessor):
    """Handles the part of the DSL that creates entities.

    In all cases the line of text starts with 'entities'.  Following that
    is a comma separated list of entity creation commands.  Each of these
    creates one or more entities.  Values are one or two words separated by
    a space.  If the second word contains the '/' character, multiple instances
    are created."""
    def __init__(self):
        """Keyword in text line indicates command is for creating entities."""
        self.keyword = "entities"
        self.factory = InstanceFactory()

    def process(self, data):
        """Convert a list of tokens into a list of instances."""
        if len(data) > 1 and data[0] == self.keyword:
            return self.createInstances(data[1:])
        else:
            return []

    def process_line(self, line, line_id, output_channels):
        """Process a line of text, if it's not for this processor, there are no entities to process."""
        for entity in self.process(line.split()):
            entity_event = EntityEvent(entity.full_name(), line_id)
            output_channels.send(json.dumps(vars(entity_event)))

    def createInstances(self, data):
        """Break list into comma separated sections, each of those becomes one or more entity instances."""
        data = [e.strip() for e in " ".join(data).split(",")]
        return [item for sublist in [self.factory.createInstances(d) for d in data] for item in sublist]

