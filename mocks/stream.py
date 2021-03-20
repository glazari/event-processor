from core.types import EventStream

class MockEventStream(EventStream):
    def __init__(self, events=None):
        if events is None:
            events = dict()
        self.events = events

    def send(self, client, event, data):
        topic = (client, event)
        if topic not in self.events:
            self.events[topic] = []
        self.events[topic].append(data)
        return True

    def list_events(self, client, event):
        topic = (client, event)
        if topic not in self.events:
            return []
        return self.events[topic]
