
class EntityExtractor:
    ENTITY_COMMAND = "create_entity"

    def __init__(self, entityFactory, abbreviations):
        self.entities = []
        self.entityFactory = entityFactory
        self.abbreviations = abbreviations

    def abbreviate(self, name):
        data = name.lower().split()
        return ''.join(d[0] for d in data)

    def abbreviate2(self, name):
        data = name.lower().split()
        if len(data) == 2:
            data[1] = data[1].upper()
        return ''.join(d[0] for d in data)

    def __call__(self, json_data, *args, **kwargs):
        if json_data['command'] == self.ENTITY_COMMAND:
            new_entity = self.entityFactory.createEntity(json_data['name'])
            self.entities.append(new_entity)
            self.abbreviations[self.abbreviate(json_data['name'])] = json_data['name']
            self.abbreviations[self.abbreviate2(json_data['name'])] = json_data['name']