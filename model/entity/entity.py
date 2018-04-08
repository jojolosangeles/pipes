

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
        remaining = list(map(lambda entity: (entity.name, entity.name.lower()), self.entities))
        for letter in name:
            remaining = list(lambda name: (name[0], self.new_name(letter, name[1])), remaining)
            remaining = [name for name in remaining if len(name) > 0]

        if len(remaining) == 1:
            return remaining[0][0]
        else:
            return ""

    def createEntity(self, name, clock, tags=[]):
        result = Entity(name, clock, tags)
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

class Entity:
    """An Entity has a name, a clock, and a set of tags for representing
    things like status or classification."""

    def __init__(self, name, clock, tags, acceptableValueStrategy = DefaultAcceptableValueStrategy()):
        self.name = name
        self.clock = clock
        self.tags = tags
        self.acceptableValueStrategy = acceptableValueStrategy

        # an entity keeps track of the messages it has sent and received
        self.sent = 0
        self.received = 0

        # an entity has a key-value store of distributed key-value pairs
        self.kvStore = {}
        self.rejected = 0  # the key-value settings that were rejected by strategy

    def process(self, value):
        """A value has a name, a timestamp (optional, used in some
        distribution strategies like last-write-wins), and an actual value."""
        self.received += 1

        if self.acceptableValueStrategy.checkProposedValue(self.kvStore.get(value.name), value):
            self.kvStore[value.name] = value
            # set time if it's not set yet
            if value.timestamp == 0:
                value.timestamp = self.clock.time()
        else:
            self.rejected += 1

    def get(self, key):
        return self.kvStore.get(key)

    def time(self):
        return self.clock.time()