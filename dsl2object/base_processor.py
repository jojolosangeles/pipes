class BaseProcessor:
    def set_streams(self, output_stream, monitor_stream):
        self.output_stream = output_stream
        self.monitor_stream = monitor_stream

    def monitor_line(self, line):
        self.monitor_stream.monitor_send(line, self.output_stream.id)

    def monitor_event(self, event, senderId):
        self.monitor_stream.monitor_event(event, senderId, self.output_stream.id)

class EchoProcessor(BaseProcessor):
    def process_line(self, line):
        line = line.strip()
        super().monitor_line(line)
        self.output_stream.write(line)