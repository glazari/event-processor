import jsonschema
from jsonschema import validators
from core.types import EventStream
from core.types import SchemaStorage


class EventProcessor:
    def __init__(self, sender: EventStream, storage: SchemaStorage):
        self.sender = sender
        self.storage = storage
        self.schema_validator = validators.validator_for(False)

    def register_event(self, event_name, client, event_schema):
        try:
            self.schema_validator.check_schema(event_schema)
        except jsonschema.SchemaError:
            return False

        success = self.storage.register_event(
            event_name, client, event_schema
        )
        return success

    def get_event(self, event_name, client):
        event_schema = self.storage.get_event(event_name, client)
        return event_schema

    def list_registered_events(self, client):
        registered_events = [
                (c, e)
                for c, e, _ in self.storage.list_events()
                if c == client
        ]
        return registered_events

    def receive_event(self, client: str, event_name: str, data: dict):
        pass

    def _valid_event(self, data: dict, schema: dict):
        try:
            jsonschema.validate(data, schema)
            out = True
        except jsonschema.ValidationError:
            out = False
        return out
