import pytest

from model.factory.event_factory import EventFactory

@pytest.fixture
def event_factory(abbreviations):
    return EventFactory(abbreviations)

@pytest.fixture
def abbreviations():
    return {}

def test_null_event(event_factory, abbreviations):
    event = event_factory.create_instance("blah", {})
    assert(event.__class__.__name__ == "NullEvent")

def test_send_message_event(event_factory, abbreviations):
    json_data = { "message": "test message", "from_entity": "fe", "to_entity": "te", "delay": "3" }
    event = event_factory.create_instance("send_message", json_data)
    assert(event.__class__.__name__ == "SendMessageEvent")

def test_set_state_event(event_factory, abbreviations):
    json_data = { "state": "test state", "name": "e", "delay": "3" }
    event = event_factory.create_instance("set_state", json_data)
    assert(event.__class__.__name__ == "SetStateEvent")

def test_sync_event(event_factory, abbreviations):
    json_data = { "sync": "sync", "entities": "1,2,3" }
    event = event_factory.create_instance("sync", json_data)
    assert(event.__class__.__name__ == "SyncEvent")