import json

from kafka import KafkaProducer

from core.types import EventStream


class KafkaEventStream(EventStream):
    def __init__(self, servers):
        self.kafka = KafkaProducer(
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            api_version="0.10",
            bootstrap_servers=servers,
        )

    def send(self, client, event, data):
        topic = f"{client}.{event}"
        self.kafka.send(topic, data)
        return True

    def __del__(self):
        self.kafka.close()


if __name__ == '__main__':
    es = KafkaEventStream("kafka:9092")
    fruit = {"fruit":"apple"}
    es.send("sponge_bob", "fruit_event", fruit)
    es.send("sponge_bob", "fruit_event", fruit)
    es.send("sponge_bob", "fruit_event", fruit)

    color = {"color":"blue"}
    es.send("sponge_bob", "color_event", color)
    es.send("sponge_bob", "color_event", color)
    es.send("sponge_bob", "color_event", color)
