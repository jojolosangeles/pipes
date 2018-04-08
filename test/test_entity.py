import pytest

from model.entity.distributed_value import DistributedValue
from model.entity.entity import EntityFactory, LastWriteWinsAcceptableValueStrategy
from model.time.clock import Universe, Clock


@pytest.fixture
def entity_factory():
    return EntityFactory()

@pytest.fixture
def distributed_value_1():
    return DistributedValue("dv1", 1, 0)

@pytest.fixture
def distributed_value_2():
    return DistributedValue("dv2", 2, 10)

@pytest.fixture
def distributed_value_1_later():
    return DistributedValue("dv1", 11, 110)

@pytest.fixture
def distributed_value_2_later():
    return DistributedValue("dv2", 22, 220)

def test_create_entity(entity_factory):
    entity = entity_factory.createEntity("entity1", Clock())
    assert(entity.time() == 0)
    assert(entity.name == "entity1")
    assert(entity.sent == 0)
    assert(entity.received == 0)

def test_set_value_in_entity(entity_factory, distributed_value_1):
    entity = entity_factory.createEntity("e2", Clock())
    assert(entity.time() == 0)
    assert(entity.name == "e2")
    assert(entity.sent == 0)
    assert(entity.received == 0)
    assert(entity.rejected == 0)
    entity.process(distributed_value_1)
    assert(entity.time() == 0)
    assert(entity.name == "e2")
    assert(entity.sent == 0)
    assert(entity.received == 1)
    assert(entity.rejected == 0)

def test_set_value_twice_in_entity(entity_factory, distributed_value_1, distributed_value_2):
    entity = entity_factory.createEntity("e2", Clock())
    Universe.tick()
    entity.process(distributed_value_1)
    assert(entity.time() == 1)
    assert(entity.name == "e2")
    Universe.tick()
    entity.process(distributed_value_2)
    assert(entity.time() == 2)
    dv1 = entity.get("dv1")
    assert(dv1.timestamp == 1)
    dv2 = entity.get("dv2")
    assert(dv2.timestamp == 10)

def test_set_value_twice_in_entity(entity_factory, distributed_value_1, distributed_value_2, distributed_value_1_later, distributed_value_2_later):
    entity = entity_factory.createEntity("e2", Clock())
    Universe.tick()
    Universe.tick()
    Universe.tick()
    entity.process(distributed_value_1)
    assert(entity.time() == 3)
    assert(entity.name == "e2")
    dv1 = entity.get("dv1")
    assert(dv1.timestamp == 3)
    entity.process(distributed_value_1_later)
    dv1 = entity.get("dv1")
    assert(dv1.timestamp == 110)

def test_set_value_twice_LWW(entity_factory, distributed_value_1, distributed_value_2, distributed_value_1_later, distributed_value_2_later):
    entity = entity_factory.createEntity("e2", Clock())
    assert(entity.time() == 0)
    entity.acceptableValueStrategy = LastWriteWinsAcceptableValueStrategy()
    Universe.tick()
    Universe.tick()
    Universe.tick()
    entity.process(distributed_value_2_later)
    assert(entity.time() == 3)
    assert(entity.name == "e2")
    dv2 = entity.get("dv2")
    assert(dv2.timestamp == 220)
    entity.process(distributed_value_2)
    assert(entity.rejected == 1)
    dv2 = entity.get("dv2")
    assert(dv2.timestamp == 220)