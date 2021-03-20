from core.types import Storage


class MockStorage(Storage):
    def __init__(self, starter=None):
        if starter is None:
            starter = dict()
        self.events_schemas = starter

    def register_event(self, event_name, client, event_schema):
        key = (client, event_name)
        if key in self.events_schemas:
            return False

        self.events_schemas[key] = event_schema
        return True

    def get_event(self, event_name, client):
        key = (client, event_name)
        if key not in self.events_schemas:
            return None

        return self.events_schemas[key]

    def list_events(self):
        for key,schema in self.events_schemas.items():
            client, event_name = key
            yield (client, event_name, schema)
