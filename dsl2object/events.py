global_event_id = 0

class BaseEvent:
    def __init__(self, command_key, originating_event_id):
        self.event_id = self.genIdValue()
        self.originating_event_id = originating_event_id
        self.command = command_key

    @classmethod
    def genIdValue(cls):
        global global_event_id
        global_event_id += 1
        return global_event_id

class SyncEvent(BaseEvent):
    COMMAND_KEY = 'sync'

    def __init__(self, entities):
        super().__init__(self.COMMAND_KEY, 0)
        self.entities = entities

class StateEvent(BaseEvent):
    COMMAND_KEY = 'set_state'

    def __init__(self, name, state, delay, originating_event_id):
        super().__init__(self.COMMAND_KEY, originating_event_id)
        self.name = name
        self.state = state
        self.delay = delay

class EntityEvent(BaseEvent):
    COMMAND_KEY = 'create_entity'

    def __init__(self, name, originating_event_id):
        super().__init__(self.COMMAND_KEY, originating_event_id)
        self.name = name


class FloatEvent(BaseEvent):
    COMMAND_KEY = 'set_key_value'

    def __init__(self, field_name, type, precision, value, originating_event_id):
        super().__init__(self.COMMAND_KEY, originating_event_id)
        self.type = type
        self.precision = precision
        self.field_name = field_name
        if type == 'float':
            self.value = float(value)
        else:
            self.value = value

class MessageEvent(BaseEvent):
    COMMAND_KEY = 'send_message'

    def __init__(self, from_entity, delay, message, to_entity, originating_event_id):
        super().__init__(self.COMMAND_KEY, originating_event_id)
        self.from_entity = from_entity
        self.delay = delay
        self.message = message
        self.to_entity = to_entity