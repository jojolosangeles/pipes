import sys
from pipes.processors.passthrough import PassThrough
from dsl2object.dsl_engine import DSL_Engine
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
                self.collecting_sequence = False
        elif value == self.start_word:
            self.collecting_sequence = True
        return False

if __name__ == "__main__":
    inputParameterExtractor = ListExtractor("input", [ "processor", "output" ])
    outputParameterExtractor = ListExtractor("output", [ "processor", "input" ])
    processorParameterExtractor = ListExtractor("processor", [ "input", "output" ])
    input_channel_parameters = [p for p in sys.argv if inputParameterExtractor(p)]
    output_channel_parameters = [p for p in sys.argv if outputParameterExtractor(p)]
    processor_parameters = [p for p in sys.argv if processorParameterExtractor(p)]
    channelFactory = ChannelFactory()
    input_channel = channelFactory.createInputChannel(input_channel_parameters)
    output_channel = channelFactory.createOutputChannel(output_channel_parameters)
    processor = channelFactory.createProcessor(processor_parameters, output_channel)
    pipe = Pipe(input_channel, output_channel, processor)
    pipe.activate()
    print("test is over")
