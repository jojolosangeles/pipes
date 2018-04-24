
class EntityExtractor:
    def __init__(self, entityFactory):
        self.entities = []
        self.entityFactory = entityFactory

    def __call__(self, json_data, *args, **kwargs):
        if json_data['command'] == "create_entity":
            self.entities.append(self.entityFactory.createEntity(json_data['name']))