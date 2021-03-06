import sys

from pipes.channels.channel_factory import ChannelFactory

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

class ListExtractor:
    def __init__(self, start_word, terminating_words):
        self.start_word = start_word
        self.terminating_words = terminating_words
        self.collecting_sequence = False

    def __call__(self, value, *args, **kwargs):
        if self.collecting_sequence:
            if not value in self.terminating_words:
                return True
            else:
                self.collecting_sequence = (value == self.start_word)
        elif value == self.start_word:
            self.collecting_sequence = True
        return False
