import sys

# TODO these are 'not used' but they are loaded using 'import_module'
# which needs these present, otherwise I get an error saying they don't exist.
# I don't understand why
from pipes.processors.passthrough import PassThrough
from dsl2object.dsl_engine import DSL_Engine
from timelines.timeline_engine import TimelineEngine

# these are used
from pipes.channels.stream import StreamInChannel, StreamOutChannel
from pipes.channels.websocket import WebsocketInChannel, WebsocketOutChannel
from pipes.rabbitmq import RabbitMQ
from util.tracer import Tracer

tracer = Tracer(False)

class UnspecifiedChannel:
    def __init__(self, params):
        self.params = params

    def send(self, message):
        print("UNSPECIFIED SEND CHANNEL: {}".format(self.params))

    def receive(self, line_processor):
        print("UNSPECIFIED RECEIVE CHANNEL: {}".format(self.params))

def import_module(name):
    """from https://stackoverflow.com/questions/547829/how-to-dynamically-load-a-python-class?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    """
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

class ChannelFactory:

    @tracer
    def createInputChannel(self, input_channel_params):
        channel_type = input_channel_params[0]
        if channel_type == "stream":
            if input_channel_params[1] == "stdin":
                return StreamInChannel(sys.stdin)
            elif input_channel_params[1] == "file":
                return StreamInChannel(open(input_channel_params[2], "r"))
        elif channel_type == "rabbitmq":
            host = input_channel_params[1]
            queue = input_channel_params[2]
            return RabbitMQ(host, queue)
        elif channel_type == "websocket":
            port = int(input_channel_params[1])
            return WebsocketInChannel(port)
        else:
            return UnspecifiedChannel(input_channel_params)

    @tracer
    def createOutputChannels(self, output_channel_parameters):
        parameter_offset = 0
        result = []
        while parameter_offset < len(output_channel_parameters):
            number_parameters_used, output_channel = self.createOutputChannel(output_channel_parameters[parameter_offset:])
            result.append(output_channel)
            parameter_offset += number_parameters_used
        return result

    def createOutputChannel(self, output_channel_parameters):
        channel_type = output_channel_parameters[0]
        if channel_type == "stream":
            if output_channel_parameters[1] == "stdout":
                return 2, StreamOutChannel(sys.stdout)
            elif output_channel_parameters[1] == "file":
                return 3, StreamOutChannel(open(output_channel_parameters[2], "w"))
        elif channel_type == "rabbitmq":
            host = output_channel_parameters[1]
            queue = output_channel_parameters[2]
            return 3, RabbitMQ(host, queue)
        elif channel_type == "websocket":
            port = int(output_channel_parameters[1])
            return 2, WebsocketOutChannel(port)
        else:
            return 2, UnspecifiedChannel(output_channel_parameters)

    @tracer
    def createProcessor(self, processor_parameters, output_channels):
        path = processor_parameters[0]
        klass = import_module(path)
        return klass(output_channels)

