import sys
import json
import random
import time

import requests


class Client:
    base_path = "http://localhost:5000"

    def register(self, client, event, schema):
        url = f"{self.base_path}/{client}/{event}/register_event"
        data = {"event_schema": json.dumps(schema)}
        resp = requests.post(url, data=data)
        return resp.json()

    def send(self, client, event, payload):
        url = f"{self.base_path}/{client}/{event}/send_event"
        data = {"event": json.dumps(payload)}
        resp = requests.post(url, data=data)
        return resp.json()

    def get_schema(self, client, event):
        url = f"{self.base_path}/{client}/{event}/schema"
        resp = requests.get(url)
        return resp.json()

    def list_events(self, client):
        url = f"{self.base_path}/{client}/list_events"
        resp = requests.get(url)
        return resp.json()


def send_events(client_name, event_name, schema, get_event):
    client = Client()
    print(f"using client named: {client_name}")
    print(f"registering new event named: {event_name}")
    client.register(client_name, event_name, schema)

    while True:
        event = get_event()
        print("sending event:", event)
        client.send(client_name, event_name, event)
        time.sleep(1)

def send_fruits():
    client_name = "SpongeBob"
    event_name = "Fruits"
    schema = {"type":"object", "required":["fruit"]}
    fruits = [
        "apple", "banana", "orange", "pineapple",
        "pear", "grapes", "watermelon", "lemon",
        "strawberry", "blueberry",
    ]
    get_event = lambda : {"fruit":random.choice(fruits)}

    send_events(client_name, event_name, schema, get_event)

def send_colors():
    client_name = "SpongeBob"
    event_name = "Colors"
    schema = {"type":"object", "required":["color"]}
    colors = [
        "blue", "red", "pink", "black", "white", "green",
        "yellow", "purple", "violet", "orange", "brown",
        "cyan", "gray",
    ]
    get_event = lambda : {"color":random.choice(colors)}

    send_events(client_name, event_name, schema, get_event)


def usage():
    msg ="""
    Usage:
    There are 2 example options to choose from:
    
    - python producer.py fruits
    - python producer.py colors

    """
    print(msg)


if __name__ == "__main__":
    args = sys.argv

    if len(args) != 2:
        usage()
        sys.exit(1)

    if args[1] == 'fruits':
        send_fruits()
    elif args[1] == 'colors':
        send_colors()
    else:
        usage()
        sys.exit(1)
