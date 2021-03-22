# Event Processor

This is a sample project for an event gateway that receives events from various
clients validates that they satisfy a certain schema and the persist the events
in a publisher-subscriber type database for further processing.

## Requirements

This project uses
- [docker](https://docs.docker.com/get-docker/)
- [docker-compose](https://docs.docker.com/compose/install/)
- [pipenv](https://pypi.org/project/pipenv/)

Make sure that you have them installed before you start the following setup.

## setup

To setup your local python environment with the correct dependencies just
run:

```bash
# setup local python environment
pipenv shell
pipenv install --dev
```

## Example Usage

There is a `Fruits` example ready for you to try. First startup the docker 
containers.

```bash
docker-compose up
```

The first run will download the images so it might take a while.
In a new terminal run the listen.sh script to listen for events on kafka.

```bash
./listen.sh fruits
# Listening to events from topic: SpongeBob.Fruits
```

On yet another terminal start the producer with the producer.py script.

```bash
python producer.py fruits
# using client named: SpongeBob
# registering new event named: Fruits
# sending event: {'fruit': 'apple'}
# sending event: {'fruit': 'banana'}
```

As soon as the producer starts sending events you should see the same events 
appearing on the consumer side.

There is a very similar example for `Colors` that you can run on 2 new terminal
to demonstrate the ability to deal with multiple event streams at a time.

```bash
./listen.sh colors
python producer.py colors
```


## Parts


- GRPAH description

### Business Logic

Following an [Hexagonal Architecture](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)), I try too keep all of the business
logic in a single place and isolated from the components that interact with the
outside world, that is the user interface and the backend storage. There are 2 
important benefits to this approach. The first is that the outside world is
messy and avoiding it in te business logic makes it much easier to test. The
second big benefit is that the outside components are forced to implement a 
very clear interface to interact with the business logic, this makes it easy
to swap out components for a simillar function, for example, to swapout a 
kafka producer to a kinesis producer.

```bash
core/event_processor.py
```

Main Business functions:
- recieve_event
- register_event 
- get_event_schema
- list_registerd_events

The `receive_event` is the main businesse funcion, it will receive an
event, validate it against a given schema and if valid, publish it
to an event stream. In order to know which schema to use to validate
we need to first `register_event`.

External world components:
- web api
- Schema Storage
- Event Stream

### Tests

Tests are very underrated, in my opinion. Tests allows you to make big changes
with confidence, they allow new comers to have example executions the can learn
from, they document expected behavior.

This project uses [pytest](https://docs.pytest.org/en/stable/) for the tests and you can run the full suit by
running:

```bash
pytest tests
```

You should see and output like this:

```txt
================================= test session starts =========================
collected 8 items

tests/core/event_processor_test.py ....                                 [ 50%]
tests/web/endpoints_test.py ....                                        [100%]

================================== 8 passed in 0.47s ==========================
```

### Schema Type

To validate the incoming events we need a way to describe what is a valid
event. This is called a schema of the event. There are several kinds of 
schemas that could be used for this kind of project.

Schema Type:
- [JSONschema](https://json-schema.org/)
- [Avro](https://en.wikipedia.org/wiki/Apache_Avro)
- [Protobuf](https://developers.google.com/protocol-buffers)

I chose to use jsonschema for this project because it is easy to use and since
it is a pure text format it is also easy to debug.


### HTTP endpoint

The input interface that is exposed to the world is a [Flask http server](https://flask.palletsprojects.com/en/1.1.x/). With
endpoints that mimic the core business functions.

```bash
web/endpoints.py
```

HTTP endpoints:
- POST /<client>/<event-name>/send_event
- POST /<client>/<event-name>/register_event
- GET /<client>/<event-name>/schema
- GET /<client>/list_events

when the docker-compose is active these endpoints can be accessed on 
`localhost:5000`. There is also a simple example of calling the endpoints
in the `quick_test.py` file.


### Schema Storage

The schema storage can be any database that supports a key value access pattern.
There are also some services specialised in schema registry.

- [PostgreSQL](https://www.postgresql.org/)
- [Schema registry](https://docs.confluent.io/platform/current/schema-registry/index.html)

I chose to use postgres because of previous familiarity.


### Event Stream

The event stream can be any database that supports a publisher subscriber 
access pattern. I chose to use kafka because I already had experience setting
up docker-compose to run with it.


Some other options
- [kafka](https://kafka.apache.org/)
- [kinesis](https://aws.amazon.com/kinesis/)
- [rabbitMQ](https://www.rabbitmq.com/)
- [redis](https://redis.io/topics/pubsub)



