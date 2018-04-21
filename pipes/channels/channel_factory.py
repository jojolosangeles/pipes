import sys
from pipes.rabbitmq import RabbitMQ

class Tracer:
    def __init__(self):
        self.enabled = True

    def __call__(self, f):
        def wrap(*args, **kwargs):
            if self.enabled:
                print("{}{}".format(f.__name__, args[1:]))
            return f(*args, **kwargs)
        return wrap

tracer = Tracer()

class StreamInChannel:
    """This channel implements 'incoming_channel' protocol, 'receive(line_processor'.
    This is for any stream, like stdin or a file.
        """
    def __init__(self, stream):
        self.stream = stream

    def receive(self, line_processor):
        while True:
            line = self.stream.readline().strip()
            line_processor(line)
            if line == "exit":
                break

class StreamOutChannel:
    """This channel implements 'incoming_channel' protocol, 'receive(line_processor'.
    This is for any stream, like stdin or a file.
        """
    def __init__(self, stream):
        self.stream = stream

    def send(self, message):
        self.stream.write(message)

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
    def __init__(self):
        pass

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
        else:
            return UnspecifiedChannel(input_channel_params)

    @tracer
    def createOutputChannel(self, output_channel_parameters):
        channel_type = output_channel_parameters[0]
        if channel_type == "stream":
            if output_channel_parameters[1] == "stdout":
                return StreamOutChannel(sys.stdout)
            elif output_channel_parameters[1] == "file":
                return StreamOutChannel(open(output_channel_parameters[2], "w"))
        elif channel_type == "rabbitmq":
            host = output_channel_parameters[1]
            queue = output_channel_parameters[2]
            return RabbitMQ(host, queue)
        else:
            return UnspecifiedChannel(output_channel_parameters)

    @tracer
    def createProcessor(self, processor_parameters, output_channel):
        path = processor_parameters[0]
        klass = import_module(path)
        return klass(output_channel)

