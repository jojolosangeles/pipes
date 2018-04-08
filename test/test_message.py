import pytest

from model.services.message import MessageService
from model.time.clock import Universe


class Target:
    def __init__(self):
        self.processed_count = 0

    def process(self, event):
        self.processed_count += 1

@pytest.fixture
def target():
    return Target()

@pytest.fixture
def msg_source():
    return "Message Source"

def test_message_send(msg_source, target):
    MessageService.send(msg_source, target, "{ x: 1 }", 1)
    assert(len(MessageService.queued_events) == 1)
    assert(target.processed_count == 0)
    MessageService.tick()
    assert(target.processed_count == 1)

def test_message_send2(msg_source, target):
    MessageService.send(msg_source, target, "{ x: 1 }", 3)
    assert(len(MessageService.queued_events) == 1)
    assert(target.processed_count == 0)
    MessageService.tick()
    assert(target.processed_count == 0)
    MessageService.tick()
    assert(target.processed_count == 0)
    MessageService.tick()
    assert(target.processed_count == 1)
    assert(len(MessageService.queued_events) == 0)

def test_message_universe_ticks(msg_source, target):
    Universe.registered_tickers.append(MessageService)
    MessageService.send(msg_source, target, "{ x: 1 }", 3)
    assert(len(MessageService.queued_events) == 1)
    assert(target.processed_count == 0)
    Universe.tick()
    assert(target.processed_count == 0)
    Universe.tick()
    assert(target.processed_count == 0)
    Universe.tick()
    assert(target.processed_count == 1)
    assert(len(MessageService.queued_events) == 0)