import io

import pytest

from ddbsim import MonitoredStream
from dsl2object.message_dsl import MessageDSL

@pytest.fixture
def str_output():
    return MonitoredStream(io.StringIO(), "str_output")

@pytest.fixture
def message_factory(str_output):
    result = MessageDSL()
    result.set_streams(str_output)
    return result

def test_messageDSL(message_factory, str_output):
    message_factory.process_line("NodeA (3)x=2 NodeB", 1)
    expected_result = '{"event_id": 1, "originating_event_id": 1, "command": "send_message", "from_entity": "NodeA", "delay": 3, "message": "x=2", "to_entity": "NodeB"}\n'
    assert(message_factory.output_stream.stream.getvalue() == expected_result)
