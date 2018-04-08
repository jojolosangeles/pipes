import pytest

from model.time.clock import Clock, Universe

@pytest.fixture
def start_time_1():
    return 0

def test_clock_initial(start_time_1):
    clock = Clock(start_time_1)
    assert(clock.time() == 0)

def test_clock_tick(start_time_1):
    clock = Clock(start_time_1)
    Universe.tick()
    assert(clock.time() == 1)

def test_clock_tick2(start_time_1):
    clock = Clock(start_time_1)
    Universe.tick()
    Universe.tick()
    assert(clock.time() == 2)