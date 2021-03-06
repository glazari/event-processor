from core.event_processor import EventProcessor
from schema_storages.mock import MockSchemaStorage
from event_streams.mock import MockEventStream


def test_event_processor_valid_event():
    test_cases = [
        {
            "name": "valid event",
            "data": {"fruit":"apple","color":"blue"},
            "schema": {
                "type":"object",
                "required": ["color", "fruit"],
                "properties": {
                    "fruit":{"type":"string", "description":"name of fruit"},
                    "color":{"type":"string", "description":"name of color"},
                },
                "additionalProperties": False,
            },
            "out": True
        },
        {
            "name": "invalid event",
            "data": {"fruit":"apple"},
            "schema": {
                "type":"object",
                "required": ["color", "fruit"],
                "properties": {
                    "fruit":{"type":"string", "description":"name of fruit"},
                    "color":{"type":"string", "description":"name of color"},
                },
                "additionalProperties": False,
            },
            "out": False
        },
    ]


    for tc in test_cases:
        ep = EventProcessor(MockEventStream(), MockSchemaStorage())
        got = ep._valid_event(tc["data"], tc["schema"])
        assert got == tc["out"], f"Error on test_case: {tc['name']}"


def test_event_processor_register_event():
    test_cases = [
        {
            "name": "succesfully register",
            "client": "client1",
            "event_name": "new_event",
            "schema": {"type":"object","required":["color"]},
            "storage": MockSchemaStorage(),
            "success":True,
        },
        {
            "name": "already registered",
            "client": "client1",
            "event_name": "old_event",
            "schema": {"type":"object","required":["color"]},
            "storage": MockSchemaStorage({("client1","old_event"): {}}),
            "success":False,
        },
        {
            "name": "invalid schema",
            "client": "client1",
            "event_name": "new_event",
            "schema": {"type":"random_type"},
            "storage": MockSchemaStorage(),
            "success":False,
        },
    ]

    for tc in test_cases:
        ep = EventProcessor(MockEventStream(), tc["storage"])
        got = ep.register_event(tc["client"], tc["event_name"], tc["schema"])
        assert got == tc["success"], f"Error on test_case: {tc['name']}"

        if not tc["success"]:
            continue

        got = ep.get_event(tc["client"], tc["event_name"])
        assert got == tc["schema"], f"Error, stored schema does not match registerd: {tc['name']}"

def test_event_processor_list_registerd_events():
    test_cases = [
        {
            "name": "base case",
            "storage":MockSchemaStorage({
                ("a","e1"): "",
                ("a","e2"): "",
                ("b","e1"): "",
            }),
            "query_client":"a",
            "contains": [
                ("a","e1"),
                ("a","e2"),
            ],
            "not contains": [
                ("b","e1"),
            ],
        },
    ]

    for tc in test_cases:
        ep = EventProcessor(MockEventStream(), tc["storage"])
        registered_events = ep.list_registered_events(tc["query_client"])
        for event in tc["contains"]:
            assert event in registered_events, f"{tc['name']}: '{event}' not found"

        for event in tc["not contains"]:
            assert event not in registered_events, f"{tc['name']}: '{event}' should not be present"


def test_event_processor_recieve_event():
    test_cases = [
        {
            "name": "valid event",
            "data": {"color":"blue"},
            "client": 'client1',
            "event": "event_name",
            "storage": MockSchemaStorage({
                ("client1","event_name"): {"type":"object","required":["color"]},
            }),
            "success": True,
        },
        {
            "name": "invalid event",
            "data": {"name":"walter"},
            "client": 'client1',
            "event": "event_name",
            "storage": MockSchemaStorage({
                ("client1","event_name"): {"type":"object","required":["color"]},
            }),
            "success": False,
        },
        {
            "name": "unregistered event",
            "data": {"name":"walter"},
            "client": 'client1',
            "event": "new_event",
            "storage": MockSchemaStorage(),
            "success": False,
        },
    ]

    for tc in test_cases:
        es = MockEventStream()
        ep = EventProcessor(es, tc["storage"])
        success = ep.receive_event(tc['client'], tc['event'], tc['data'])

        assert success == tc["success"], f"{tc['name']}: success did not match"

        if not tc["success"]:
            continue

        events = es.list_events(tc['client'], tc['event'])
        assert tc['data'] in events, "{tc['name']}: event not stored in stream"
