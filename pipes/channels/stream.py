import sys


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
            if line == "exit" or line == "":
                break

class StreamOutChannel:
    """This channel implements 'incoming_channel' protocol, 'receive(line_processor'.
    This is for any stream, like stdin or a file.
        """
    def __init__(self, stream):
        self.stream = stream

    def send(self, message):
        self.stream.write(message)
        if self.stream == sys.stdout:
            self.stream.write("\n")
        self.stream.flush()