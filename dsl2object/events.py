class BaseEvent:
    genId = 0

    def __init__(self):
        self.event_id = self.genIdValue()

    @classmethod
    def genIdValue(cls):
        cls.genId += 1
        return cls.genId

class EntityEvent(BaseEvent):

    def __init__(self, name, id):
        super()
        self.command = 'create_entity'
        self.name = name
        self.id = id


class FloatEvent(BaseEvent):

    def __init__(self, field_name, type, precision, value):
        super()
        self.command = 'set_key_value'
        self.type = type
        self.precision = precision
        self.field_name = field_name
        if type == 'float':
            self.value = float(value)
        else:
            self.value = value

class MessageEvent(BaseEvent):

    def __init__(self, from_entity, delay, message, to_entity):
        super()
        self.command = 'send_message'
        self.from_entity = from_entity
        self.delay = delay
        self.message = message
        self.to_entity = to_entity