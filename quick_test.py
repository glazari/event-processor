import json

import requests

print("sending before registering")
resp = requests.post(
        "http://localhost:5000/client1/new_event1/send_event",
        data={"event":json.dumps({"color":"blue"})},
)
print(json.dumps(resp.json(), indent=2), "\n")

print("registering events")
resp = requests.post(
        "http://localhost:5000/client1/new_event1/register_event",
        data={"event_schema":json.dumps(
            {"type":"object", "required":["color"]})
        },
)
print(json.dumps(resp.json(), indent=2), "\n")

print("registering events again")
resp = requests.post(
        "http://localhost:5000/client1/new_event1/register_event",
        data={"event_schema":json.dumps(
            {"type":"object", "required":["color"]})
        },
)
print(json.dumps(resp.json(), indent=2), "\n")


print("sending after registering")
resp = requests.post(
        "http://localhost:5000/client1/new_event1/send_event",
        data={"event":json.dumps({"color":"blue"})},
)
print(json.dumps(resp.json(), indent=2), "\n")

print("Get event schema")
resp = requests.get(
        "http://localhost:5000/client1/new_event1/schema",
)
print(json.dumps(resp.json(), indent=2), "\n")

print("list events")
resp = requests.get(
        "http://localhost:5000/client1/list_events",
)
print(json.dumps(resp.json(), indent=2), "\n")
