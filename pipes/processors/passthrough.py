class PassThrough:
    def __init__(self, output_channel):
        self.output_channel = output_channel

    def __call__(self, line, *args, **kwargs):
        self.output_channel.send("{}\n".format(line))