class BaseProcessor:
    def set_streams(self, output_stream):
        self.output_stream = output_stream
        self.line_id = 0

    def receive_line(self):
        self.line_id += 1


class EchoProcessor(BaseProcessor):
    def process_line(self, line, line_id, output_channels):
        line = line.strip()
        for output_channel in output_channels:
            output_channel.send(line)