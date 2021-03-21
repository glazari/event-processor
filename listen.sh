client=$1
event_name=$2

topic="${client}.${event_name}"

docker-compose exec kafka opt/kafka/bin/./kafka-console-consumer.sh \
	--topic ${topic} \
	--bootstrap-server localhost:9092 \
	--offset 0 \
	--partition 0
