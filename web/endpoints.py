import json
from flask import Flask
from flask import request
from flask import current_app
from core.event_processor import EventProcessor
from mocks.storage import MockSchemaStorage
from mocks.stream import MockEventStream

app = Flask(__name__)
app.db = MockSchemaStorage()
app.es = MockEventStream()

@app.route("/<client>/<event_name>/send_event", methods=["POST"])
def send_event(client, event_name):
    ep = EventProcessor(current_app.es, current_app.db)
    data = request.form.get("event")
    if not data:
        return {"code":"FAILED", "msg": "'event' key not in data"}, 400

    data = try_json_decode(data)
    if not data:
        return {"code":"FAILED", "msg": "'event' is not a valid json"}, 400

    succ = ep.receive_event(client, event_name, data)
    if not succ:
        return {"code":"FAILED", "msg": "failed to send event"}, 400
    return {"code":"SUCCEEDED", "msg": "event sent"}, 200

@app.route("/<client>/<event_name>/register_event", methods=["POST"])
def register_event(client, event_name):
    ep = EventProcessor(current_app.es, current_app.db)
    schema = request.form.get("event_schema")
    if not schema:
        return {"code":"FAILED", "msg": "'event_schema' key not in data"}, 400

    schema = try_json_decode(schema)
    if not schema:
        return {"code":"FAILED", "msg": "'event_schema' is not a valid json"}, 400

    succ = ep.register_event(client, event_name, schema)
    if not succ:
        return {"code":"FAILED", "msg": "failed to register event"}, 400
    return {"code":"SUCCEEDED", "msg": "event registered"}, 200


@app.route("/<client>/<event_name>/schema", methods=["GET"])
def get_event_schema(client, event_name):
    ep = EventProcessor(current_app.es, current_app.db)
    schema = ep.get_event(client, event_name)
    if schema is None:
        return {"code":"FAILED", "msg": "event not registered"}, 400
    return {"code":"SUCCEEDED", "schema":schema, "msg": "schema recovered"}, 200


@app.route("/<client>/list_events", methods=["GET"])
def list_registered_events(client):
    ep = EventProcessor(current_app.es, current_app.db)
    events = ep.list_registered_events(client)
    return {"code":"SUCCEEDED", "events":events, "msg": "schema recovered"}, 200


def try_json_decode(data:str) -> dict:
    try:
        out = json.loads(data)
    except json.JSONDecodeError:
        out = None
    return out
