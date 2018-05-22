import pytest

from dsl2object.base_processor import EchoProcessor

class SendCollector:
    def __init__(self, start_value):
        self.collected = start_value

    def send(self, line):
        self.collected = line

@pytest.fixture
def collector():
    return SendCollector("zippo")

@pytest.fixture
def processor():
    return EchoProcessor()

examples = (("input", "output"),
            [("asdf", "asdf"),
             ("   ", "zippo"),
             ("  ha", "ha"),
             ("ho   ", "ho"),
             ("   heh       ", "heh")
             ])

@pytest.mark.parametrize(*examples)
def test_basic_echo(collector, processor, input, output):
    EchoProcessor().process_line(input, 1, collector)
    assert(collector.collected == output)