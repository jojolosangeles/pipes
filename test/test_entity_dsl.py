import pytest

from dsl2object.entity_dsl import EntityDSL
from dsl2object.instance import Instance

@pytest.fixture
def node_1():
    return Instance("Node", "1")

@pytest.fixture
def node_2():
    return Instance("Node", "2")

@pytest.fixture
def node_3():
    return Instance("Node", "3")

@pytest.fixture
def entity_dsl():
    return EntityDSL()

def test_entity_dsl(entity_dsl):
    result = entity_dsl.process("entities NodeABC".split())
    assert(len(result) == 1)

def test_entity_dsl2(entity_dsl, node_1):
    result = entity_dsl.process("entities Node 1".split())
    assert(len(result) == 1)
    print(type(result))
    assert(node_1.name == result[0].name)
    assert(node_1.identifier == result[0].identifier)

def test_entity_dsl2b(entity_dsl, node_1, node_2):
    result = entity_dsl.process("entities Node 1/2".split())
    assert(len(result) == 2)
    assert(node_1.name == result[0].name)
    assert(node_1.identifier == result[0].identifier)
    assert(node_2.name == result[1].name)
    assert(node_2.identifier == result[1].identifier)

def test_entity_dsl2c(entity_dsl, node_1, node_2, node_3):
    result = entity_dsl.process("entities Node 1/2, Node 3".split())
    assert(len(result) == 3)
    assert(node_1.name == result[0].name)
    assert(node_1.identifier == result[0].identifier)
    assert(node_2.name == result[1].name)
    assert(node_2.identifier == result[1].identifier)
    assert(node_3.name == result[2].name)
    assert(node_3.identifier == result[2].identifier)