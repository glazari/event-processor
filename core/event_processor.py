from typing import List
from typing import Optional

import jsonschema
from core.types import EventSender
from core.types import Storage


class EventProcessor:
    def __init__(self, sender: EventSender, storage: Storage):
        self.sender = sender
        self.storage = storage

    def register_event(self, event_name, client, event_schema):
        pass

    def list_registered_events(self, client):
        pass

    def receive_event(self, client: str, event_name: str, data: dict):
        pass

    def _valid_event(self, data: dict, schema: dict):
        try:
            jsonschema.validate(data, schema)
            out = True
        except jsonschema.ValidationError as e: 
            out = False
        return out
