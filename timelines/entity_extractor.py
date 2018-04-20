
class EntityExtractor:
    def __init__(self, entityFactory):
        self.entities = []
        self.entityFactory = entityFactory

    def process_json(self, json_data):
        if json_data['command'] == "create_entity":
            self.entities.append(self.entityFactory.createEntity(json_data['name']))