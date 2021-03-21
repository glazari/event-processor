from core.types import SchemaStorage


class PostgresSchemaStorage(SchemaStorage):
    def __init__(self, starter=None):
        pass

    def register_event(self, event_name, client, event_schema):
        pass

    def get_event(self, event_name, client):
        pass

    def list_events(self):
        pass
