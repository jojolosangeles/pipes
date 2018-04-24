import sys

from util.tracer import Tracer

tracer = Tracer(False)

class StreamInChannel:
    """This channel implements 'incoming_channel' protocol, 'receive(line_processor'.
    This is for any stream, like stdin or a file.
        """
    def __init__(self, stream):
        self.stream = stream

    def receive(self, line_processor):
        for line in self.stream:
            line = line.strip()
            #print("StreamInChannel received: {}".format(line))
            line_processor(line)
            if line == "exit" or (self.stream == sys.stdin and line == ""):
                break

class StreamOutChannel:
    """This channel implements 'incoming_channel' protocol, 'receive(line_processor'.
    This is for any stream, like stdin or a file.
        """
    def __init__(self, stream):
        self.stream = stream

    @tracer
    def send(self, message):
        self.stream.write(message)
        self.stream.write("\n")
        self.stream.flush()