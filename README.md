# kafka-python-learning
Experimental testbed to get experience with Kafka

# Single Node Basic Deployment on Docker
# https://docs.confluent.io/current/installation/docker/docs/installation/single-node-client.html

# Create a Docker Network:
$docker network create confluent

# Start ZooKeeper:
docker run -d --net=confluent --name=zookeeper -e ZOOKEEPER_CLIENT_PORT=2181 confluentinc/cp-zookeeper:5.0.0

# Start Kafka:
docker run -d --net=confluent --name=kafka -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092 -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 confluentinc/cp-kafka:5.0.0

# Create a Topic and Produce Data
docker run --net=confluent --rm confluentinc/cp-kafka:5.0.0 kafka-topics --create --topic foo --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:2181

# Verify that the topic was successfully created:
docker run --net=confluent --rm confluentinc/cp-kafka:5.0.0 kafka-topics --describe --topic foo --zookeeper zookeeper:2181

# Publish data to your new topic:
docker run --net=confluent --rm confluentinc/cp-kafka:5.0.0 bash -c "seq 42 | kafka-console-producer --request-required-acks 1 --broker-list kafka:9092 --topic foo && echo 'Produced 42 messages.'"

# Read back the message using the built-in Console consumer:
docker run --net=confluent --rm confluentinc/cp-kafka:5.0.0 kafka-console-consumer --bootstrap-server kafka:9092 --topic foo --from-beginning --max-messages 42

# Use case 1: Steam video
# https://scotch.io/tutorials/build-a-distributed-streaming-system-with-apache-kafka-and-python
# Note 1: Install ZooKeeper and Kafka https://devops.profitbricks.com/tutorials/install-and-configure-apache-kafka-on-ubuntu-1604-1/ (download Kafka: https://www.apache.org/dyn/closer.cgi?path=/kafka/0.9.0.0/kafka_2.11-0.9.0.0.tgz)
# Note 2: We must use low-resolution video source to avoid exceeding the maximum message size