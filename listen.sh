type=${1:-"not_set"}

usage() {
	echo " "
	echo "    Usage:"
	echo "    There are 2 example options to choose from:"
	echo " "
	echo "    - ./listen.sh fruits"
	echo "    - ./listen.sh colors"
	echo " "
	echo " "
}

if [ $type == "fruits" ]; then
	client=SpongeBob
	event_name=Fruits
elif [ $type == "colors" ]; then
	client=SpongeBob
	event_name=Colors
else
	usage
	exit 1
fi


topic="${client}.${event_name}"
echo "Listening to events from topic: ${topic}"

docker-compose exec kafka opt/kafka/bin/./kafka-console-consumer.sh \
	--topic ${topic} \
	--bootstrap-server localhost:9092 \
	--offset 0 \
	--partition 0
