# Event Processor

## Requirements

This project uses
- docker
- docker-compose
- pipenv

## setup

local python environment

```bash
# setup local python environment
pipenv shell
pipenv install --dev
```

## Example Usage

```bash
docker-compose up
```


```bash
./listen.sh fruits
# Listening to events from topic: SpongeBob.Fruits
```

```bash
python producer.py fruits
# using client named: SpongeBob
# registering new event named: Fruits
# sending event: {'fruit': 'apple'}
# sending event: {'fruit': 'banana'}
```

```bash
./listen.sh fruits
python producer.py fruits
```


## Parts


- GRPAH description

### Business Logic

Hexagonal style


### Schema Type

Schema Type:
- JSON?
- Avro:
- Protobuf:


### HTTP endpoint

HTTP endpoints:
- POST /send_event
- POST /register_event
- Get /event
- Get /event/<id>


### Schema Storage

- Schema registry
- kafka metadata


### Event Stream

- kafka
- kinesis
- rabbitMQ
- redis


# Tests

