class PassThrough:
    def __init__(self, output_channels):
        self.output_channels = output_channels

    def __call__(self, line, *args, **kwargs):
        self.output_channels.send("{}\n".format(line))

    def terminate(self):
        pass