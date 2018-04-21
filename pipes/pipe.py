import sys

from pipes.rabbitmq import RabbitMQ
from pipes.processors.passthrough import PassThrough

class Pipe:
    """A Pipe can only receive on an incoming channel, and send on an outgoing channel.

    Since the receiving is forever, the 'line_processor' used to process the
    received line of text, sends on the outgoing channel."""

    def __init__(self, incoming_channel, outgoing_channel, line_processor):
        """
        :param incoming_channel:  implements 'receive(line_processor)' which
          receives lines and for each line calls 'line_processor.process(line)'
        :param outgoing_channel:  implements 'send(message)',
        :param line_processor:
        :return:
        """
        self.incoming_channel = incoming_channel
        self.outgoing_channel = outgoing_channel
        self.line_processor = line_processor

    def activate(self):
        self.incoming_channel.receive(self.line_processor)

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

def default_line_processor(line):
    if line.split()[0] == "input":
        print("Whoo hoo, found special input line")
    print("Received line '{}'".format(line))

if __name__ == "__xmain__":
    print("HEYO, I am running in pipe.py, so I can add tests here")
    print("Test #1: make stdin and stdout stream in/out channel instances, and see if they work")
    print("everything typed should be echoed after pressing enter")
    print("type 'exit' to end test")
    pipe = Pipe(StreamInChannel(sys.stdin), StreamOutChannel(sys.stdout), default_line_processor)
    pipe.activate()
    print("test is over")

class InRange:
    def __init__(self):
        self.got_input = False
        self.got_output = False

    def __call__(self, value, *args, **kwargs):
        if self.got_input and not self.got_output and value != "output":
            return True
        if value == "input":
            self.got_input = True
        if value == "output":
            self.got_output = True
        return False

class OutRange:
    def __init__(self):
        self.got_output = False

    def __call__(self, value, *args, **kwargs):
        if self.got_output:
            return True
        if value == "output":
            self.got_output = True
        return False

class UnspecifiedChannel:
    def __init__(self, params):
        self.params = params

    def send(self, message):
        print("UNSPECIFIED SEND CHANNEL: {}".format(self.params))

    def receive(self, line_processor):
        print("UNSPECIFIED RECEIVE CHANNEL: {}".format(self.params))


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

class ChannelFactory:
    def __init__(self):
        pass

    @tracer
    def createInputChannel(self, input_channel_params):
        channel_type = input_channel_params[0]
        if channel_type == "stream":
            if input_channel_params[1] == "stdin":
                return StreamInChannel(sys.stdin)
            elif input_channel_parameters[1] == "file":
                return StreamInChannel(open(input_channel_params[2], "r"))
        elif channel_type == "rabbitmq":
            host = input_channel_params[1]
            queue = input_channel_params[2]
            return RabbitMQ(host, queue)
        else:
            return UnspecifiedChannel(input_channel_params)

    @tracer
    def createOutputChannel(self, output_channel_params):
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
            return UnspecifiedChannel(output_channel_params)

    def import_module(name):
        """from https://stackoverflow.com/questions/547829/how-to-dynamically-load-a-python-class?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
        """
        components = name.split('.')
        mod = __import__(components[0])
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod

    @tracer
    def createProcessor(self, path, output_channel):
        klass = self.import_module(path)
        return klass(output_channel)



if __name__ == "__main__":
    inRange = InRange()
    outRange = OutRange()
    input_channel_parameters = [p for p in sys.argv if inRange(p)]
    output_channel_parameters = [p for p in sys.argv if outRange(p)]
    channelFactory = ChannelFactory()
    input_channel = channelFactory.createInputChannel(input_channel_parameters)
    output_channel = channelFactory.createOutputChannel(output_channel_parameters)
    processor = channelFactory.createProcessor('pipes.processors.passthrough.PassThrough', output_channel)
    output_channel.send("This is a test of the output channel")
    print("type 'exit' to end test")
    pass_through = PassThrough(output_channel)
    pipe = Pipe(input_channel, output_channel, pass_through)
    pipe.activate()
    print("test is over")
