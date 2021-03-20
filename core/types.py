"""
core.types defines the central types used in the system.

These types are used as a kind of interface that allows us
to mockout external components in tests and also allows us
to switch out external components with relative ease.

For example.

To swichout the eventstream backend from kafka to kenisis
we just need to create the `send(client, event, data)`
and `list_events(client, event)`  functions.
"""
from typing import List

class EventStream:
    """ Interface for interacting with the event stream"""
    def send(self, client: str, event: str, data: dict) -> bool:
        """ Sends and event with data to the stream

        return a success bool
        """

    def list_events(self, client: str, event: str) -> List[dict]:
        """ Returns current contents of stream topic

        mostly used for testing
        """

class SchemaStorage:
    """ Interface for interacting with the SchemaStorage """
    def register_event(self, event_name: str, client: str, event_schema: dict) -> bool:
        """ registers event to Schema Storage

        returns true on success
        returns false if another event is registered with this
        """

    def get_event(self, event_name: str, client: str) -> dict:
        """ Returns the stored schema for this name, None if not present"""

    def list_events(self) -> List[tuple]:
        """ Returns a list of all events as a tuple (client, event_name, schema)
        """
