class BaseProcessor:
    def set_streams(self, output_stream):
        self.output_stream = output_stream
        self.line_id = 0

    def receive_line(self):
        self.line_id += 1

def skip_empty_lines(f):
    def checkLine(line, *args, **kwargs):
        line = line.strip()
        if len(line) > 0:
            f(line)
    return checkLine

class EchoProcessor(BaseProcessor):
    @skip_empty_lines
    def process_line(self, line, line_id, output_channels):
        output_channels.send(line)