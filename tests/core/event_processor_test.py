import jsonschema

from core.event_processor import EventProcessor
from core.types import EventSender
from core.types import Storage


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
        ep = EventProcessor(EventSender(), Storage())
        got = ep._valid_event(tc["data"], tc["schema"])
        assert got == tc["out"], f"Error on test_case: {tc['name']}"
