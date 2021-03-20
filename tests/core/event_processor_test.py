from core.event_processor import EventProcessor
from core.types import EventSender
from mocks.storage import MockStorage


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
        ep = EventProcessor(EventSender(), MockStorage())
        got = ep._valid_event(tc["data"], tc["schema"])
        assert got == tc["out"], f"Error on test_case: {tc['name']}"


def test_event_processor_register_event():
    test_cases = [
        {
            "name": "succesfully register",
            "client": "client1",
            "event_name": "new_event",
            "schema": {"type":"object","required":["color"]},
            "storage": MockStorage(),
            "success":True,
        },
        {
            "name": "already registered",
            "client": "client1",
            "event_name": "old_event",
            "schema": {"type":"object","required":["color"]},
            "storage": MockStorage({("client1","old_event"): {}}),
            "success":False,
        },
        {
            "name": "invalid schema",
            "client": "client1",
            "event_name": "new_event",
            "schema": {"type":"random_type"},
            "storage": MockStorage(),
            "success":False,
        },
    ]

    for tc in test_cases:
        ep = EventProcessor(EventSender(), tc["storage"])
        got = ep.register_event(tc["event_name"], tc["client"], tc["schema"])
        assert got == tc["success"], f"Error on test_case: {tc['name']}"

        if not tc["success"]:
            continue

        got = ep.get_event(tc["event_name"], tc["client"])
        assert got == tc["schema"], f"Error, stored schema does not match registerd: {tc['name']}"
