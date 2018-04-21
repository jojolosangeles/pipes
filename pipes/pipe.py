import sys

from pipes.rabbitmq import RabbitMQ


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

class ChannelFactory:
    def __init__(self):
        pass

    def createInputChannel(self, input_channel_params):
        print("ChannelFactory.createInputChannel {}".format(input_channel_parameters))
        channel_type = input_channel_params[0]
        if channel_type == "stream":
            if input_channel_params[1] == "stdin":
                return StreamInChannel(sys.stdin)
        elif channel_type == "rabbitmq":
            host = input_channel_params[1]
            queue = input_channel_params[2]
            print("new RabbitMQ({}, {})".format(host, queue))
            return RabbitMQ(host, queue)

    def createOutputChannel(self, output_channel_params):
        channel_type = output_channel_parameters[0]
        if channel_type == "stream":
            if output_channel_parameters[1] == "stdout":
                return StreamOutChannel(sys.stdout)
        elif channel_type == "rabbitmq":
            host = output_channel_parameters[1]
            queue = output_channel_parameters[2]
            return RabbitMQ(host, queue)

class PassThrough:
    def __init__(self, output_channel):
        self.output_channel = output_channel

    def __call__(self, line, *args, **kwargs):
        self.output_channel.send("{}\n".format(line))

if __name__ == "__main__":
    print(sys.argv)
    inRange = InRange()
    outRange = OutRange()
    input_channel_parameters = [p for p in sys.argv if inRange(p)]
    print("Input parameters: {}".format(input_channel_parameters))
    output_channel_parameters = [p for p in sys.argv if outRange(p)]
    print("Output parameters: {}".format(output_channel_parameters))
    channelFactory = ChannelFactory()
    input_channel = channelFactory.createInputChannel(input_channel_parameters)
    output_channel = channelFactory.createOutputChannel(output_channel_parameters)
    output_channel.send("This is a test of the output channel")
    print("type 'exit' to end test")
    pass_through = PassThrough(output_channel)
    pipe = Pipe(input_channel, output_channel, pass_through)
    pipe.activate()
    print("test is over")
