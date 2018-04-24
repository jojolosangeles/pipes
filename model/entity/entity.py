from model.time.clock import Clock


class EntityFactory:
    """Create entities, and keep track of all entities created."""
    def __init__(self):
        self.entities = []

    def new_name(self, letter, name):
        offset = name.find(letter)
        if offset == -1:
            return ""
        else:
            return name[(offset+1):]

    def find(self, name):
        name = name.lower()
        entity_indexes = [0]*len(self.entities)
        name_to_lowercase = list(map(lambda entity: (entity.name, entity.name.lower()), self.entities))
        for letter in name:
            name_to_lowercase = list(lambda name: (name[0], self.new_name(letter, name[1])), name_to_lowercase)
            name_to_lowercase = [name for name in name_to_lowercase if len(name) > 0]

        if len(name_to_lowercase) == 1:
            return name_to_lowercase[0][0]
        else:
            return ""

    def createEntity(self, name, clock=Clock()):
        result = Entity(name, clock)
        self.entities.append(result)
        return result

class DefaultAcceptableValueStrategy:
    """Verifying a value is acceptable for entity key-value storage.
    This default implementation accepts all values."""
    def checkProposedValue(self, currentValue, proposedValue):
        """Return True if the proposedValue is acceptable."""
        return True

class LastWriteWinsAcceptableValueStrategy:
    """Verify a value is acceptable using 'last-write-wins' strategy"""
    def checkProposedValue(self, currentValue, proposedValue):
        """The proposedValue is acceptable in two cases:
         1. if the there is no currentValue, or
         2. the proposedValue timestamp is newer than the currentValue timestamp."""
        return currentValue == None or proposedValue.timestamp > currentValue.timestamp

class MessageCounter:
    def __init__(self):
        """Track messages sent and received."""
        self.sent = 0
        self.received = 0

    def received_value(self):
        self.received += 1

    def sent_value(self):
        self.sent += 1

class KVStore:
    def __init__(self, acceptableValueStrategy):
        self.acceptableValueStrategy = acceptableValueStrategy
        self.kvStore = {}
        self.updated = 0
        self.rejected = 0

    def accept(self, value):
        if self.acceptableValueStrategy.checkProposedValue(self.kvStore.get(value.name), value):
            return True
        else:
            self.rejected += 1
            return False

    def __call__(self, key, value=None):
        if value == None:
            return self.kvStore[key]
        elif self.accept(value):
            self.kvStore[key] = value
            self.updated += 1

class Entity(MessageCounter):
    """An Entity has a name, a clock, and a set of tags for representing
    things like status or classification."""

    def __init__(self, name, clock, acceptableValueStrategy = DefaultAcceptableValueStrategy()):
        MessageCounter.__init__(self)
        self.kvStore = KVStore(acceptableValueStrategy)
        self.name = name
        self.clock = clock

    def process(self, value):
        """A value has a name, a timestamp (optional, used in some
        distribution strategies like last-write-wins), and an actual value."""
        self.received_value()

        if self.kvStore.accept(value):
            self.kvStore(value.name, value)

            # set time if it's not set yet
            if value.timestamp == 0:
                value.timestamp = self.clock.time()

    def __call__(self, key):
        return self.kvstore(key)

    def time(self):
        return self.clock.time()

    def __repr__(self):
        return self.name