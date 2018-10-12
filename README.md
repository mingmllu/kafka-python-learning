# kafka-python-learning
Experimental testbed to get experience with Kafka

# Single Node Basic Deployment on Docker
# https://docs.confluent.io/current/installation/docker/docs/installation/single-node-client.html

# Create a Docker Network:
docker run -d --net=confluent --name=zookeeper -e ZOOKEEPER_CLIENT_PORT=2181 confluentinc/cp-zookeeper:5.0.0

# Start ZooKeeper:
docker run -d --net=confluent --name=kafka -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092 -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 confluentinc/cp-kafka:5.0.0

# Start Kafka:
docker run --net=confluent --rm confluentinc/cp-kafka:5.0.0 kafka-topics --create --topic foo --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:2181

# Create a Topic and Produce Data
docker run --net=confluent --rm confluentinc/cp-kafka:5.0.0 kafka-topics --describe --topic foo --zookeeper zookeeper:2181

docker run --net=confluent --rm confluentinc/cp-kafka:5.0.0 bash -c "seq 42 | kafka-console-producer --request-required-acks 1 --broker-list kafka:9092 --topic foo && echo 'Produced 42 messages.'"

docker run --net=confluent --rm confluentinc/cp-kafka:5.0.0 kafka-console-consumer --bootstrap-server kafka:9092 --topic foo --from-beginning --max-messages 42

# Use case 1: Steam video
# https://scotch.io/tutorials/build-a-distributed-streaming-system-with-apache-kafka-and-python