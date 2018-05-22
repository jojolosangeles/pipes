class BaseProcessor:
    def receive_line(self):
        self.line_id += 1

def skip_empty_lines(f):
    def checkLine(self, line, line_id, output_channels):
        line = line.strip()
        if len(line) > 0:
            f(self, line, line_id, output_channels)
    return checkLine

class EchoProcessor(BaseProcessor):
    @skip_empty_lines
    def process_line(self, line, line_id, output_channels):
        output_channels.send(line)