class BaseProcessor:
    def set_streams(self, output_stream, monitor_stream):
        self.output_stream = output_stream
        self.monitor_stream = monitor_stream
        self.line_id = 0

    def receive_line(self):
        self.line_id += 1

    def monitor_line(self, line, line_id):
        self.monitor_stream.monitor_send(line, self.output_stream.id, line_id)

    def monitor_event(self, event):
        self.monitor_stream.monitor_event(event, self.output_stream.id)

class EchoProcessor(BaseProcessor):
    def process_line(self, line, line_id):
        line = line.strip()
        super().monitor_line(line, line_id)
        self.output_stream.write(line)