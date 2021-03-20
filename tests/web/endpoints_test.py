import unittest
import json
import pytest

from mocks.storage import MockSchemaStorage
from mocks.stream import MockEventStream
from web.endpoints import app

class EndpointTests(unittest.TestCase):

    def setUp(self):
        app.testing = True
        app.db = MockSchemaStorage()
        app.es = MockEventStream()

        self.client = app.test_client()
        self.app = app

    def test_send_event(self):
        test_cases = [
            {
                "name":"existing event",
                "db": MockSchemaStorage({
                    ("client1","event_name"): {"type":"object","required":["color"]},
                }),
                "client": "client1",
                "event_name": "event_name",
                "data": {"color":"blue"},
                "status_code": 200,
                "code": "SUCCEEDED",
            },
            {
                "name":"new event",
                "db": MockSchemaStorage(),
                "client": "client1",
                "event_name": "event_name",
                "data": {"color":"blue"},
                "status_code": 400,
                "code": "FAILED",
            },
            {
                "name":"invalid schema",
                "db": MockSchemaStorage({
                    ("client1","event_name"): {"type":"object","required":["color"]},
                }),
                "client": "client1",
                "event_name": "event_name",
                "data": {"name":"Jonas"},
                "status_code": 400,
                "code": "FAILED",
            },
        ]

        for tc in test_cases:
            self.app.db = tc['db']
            rv = self.client.post(
                f"/{tc['client']}/{tc['event_name']}/send_event",
                data={"event": json.dumps(tc['data'])},
            )

            assert rv.status_code == tc['status_code'], f"{tc['name']}: wrong status_code"
            assert rv.json['code'] == tc['code'], f"{tc['name']}: wrong code"

    def test_register_event(self):
        test_cases = [
            {
                "name":"new event",
                "db": MockSchemaStorage(),
                "client": "client1",
                "event_name": "event_name",
                "schema": {"type":"object","required":["color"]},
                "status_code": 200,
                "code": "SUCCEEDED",
            },
            {
                "name":"existing event",
                "db": MockSchemaStorage({
                    ("client1","event_name"): {},
                }),
                "client": "client1",
                "event_name": "event_name",
                "schema": {"type":"object","required":["color"]},
                "status_code": 400,
                "code": "FAILED",
            },
            {
                "name":"invalid schema",
                "db": MockSchemaStorage(),
                "client": "client1",
                "event_name": "event_name",
                "schema": {"type":"random_type"},
                "status_code": 400,
                "code": "FAILED",
            },
        ]

        for tc in test_cases:
            self.app.db = tc['db']
            rv = self.client.post(
                f"/{tc['client']}/{tc['event_name']}/register_event",
                data={"event_schema": json.dumps(tc['schema'])},
            )

            assert rv.status_code == tc['status_code'], f"{tc['name']}: wrong status_code"
            assert rv.json['code'] == tc['code'], f"{tc['name']}: wrong code"
        pass

    def test_event_schema(self):
        test_cases = [
            {
                "name":"existing event",
                "db": MockSchemaStorage({
                    ("client1","event_name"): {"type":"object","required":["color"]},
                }),
                "client": "client1",
                "event_name": "event_name",
                "status_code": 200,
                "code": "SUCCEEDED",
                "schema": {"type":"object","required":["color"]},
            },
        ]

        for tc in test_cases:
            self.app.db = tc['db']
            rv = self.client.get(
                f"/{tc['client']}/{tc['event_name']}/schema",
            )

            assert rv.status_code == tc['status_code'], f"{tc['name']}: wrong status_code"
            assert rv.json['code'] == tc['code'], f"{tc['name']}: wrong code"

            if tc['code'] != 'SUCCEEDED':
                continue

            assert rv.json['schema'] == tc['schema'], f"{tc['name']}: wrong code"

    def test_list_events(self):
        test_cases = [
            {
                "name":"existing event",
                "db": MockSchemaStorage({
                    ("client1","event_name"): {"type":"object","required":["color"]},
                }),
                "client": "client1",
                "status_code": 200,
                "code": "SUCCEEDED",
                "contains": [["client1","event_name"],],
            },
        ]

        for tc in test_cases:
            self.app.db = tc['db']
            rv = self.client.get(f"/{tc['client']}/list_events")

            assert rv.status_code == tc['status_code'], f"{tc['name']}: wrong status_code"
            assert rv.json['code'] == tc['code'], f"{tc['name']}: wrong code"

            if tc['code'] != 'SUCCEEDED':
                continue

            for event in tc['contains']:
                assert event in rv.json['events'], f"{tc['name']}: missing event"
