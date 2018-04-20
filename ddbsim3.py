from dsl2object.dsl_engine import DSL_Engine
from pipes.rabbitmq import RabbitMQ


class PipelineProcessor:

    def __init__(self, input_queue_name, output_queue_name, output_router, line_processor):
        self.input_queue = RabbitMQ('localhost', input_queue_name, line_processor)
        output_router.set_output_queue(output_queue_name)

    def start(self):
        self.input_queue.receive()

if __name__ == "__main__":
    dsl_engine = DSL_Engine()
    pp = PipelineProcessor('intext', 'jsonq', dsl_engine, dsl_engine.process_line)
    pp.start()

