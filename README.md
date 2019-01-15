
## Set up Kafka Broker in Docker Environment

This is a preferred approach to deplying a Kafka broker.

See https://github.com/wurstmeister/kafka-docker. Assume that you have installed docker and docker-compose. Take the simple steps as below to bring up kafka conatiners:

1. Check out the kafka-docker files including docker compose configuration.

```
$ git clone https://github.com/wurstmeister/kafka-docker.git
```
2. Change directory to "kafka-docker", open the file "docker-compose-single-broker.yml", and change the KAFKA_ADVERTISED_HOST_NAME to match your docker host IP address:

3. Run the command:
```
$ docker-compose -f docker-compose-single-broker.yml up -d
```

## Install Apache ZooKeeper and Kafka servers

*If you has installed Kafka in docker, you can directly go to the section "Install kafka-python at the client side"*


The following steps apply to both Ubuntu 16.04 and 18.04 LTS servers.

### Requirements:

Ubuntu 16.04 LTS or 18.04 LTS

A non-root user with sudo privileges

OpenJDK 8 installed on your server. Kafka server won't be started in the later JDK due to a bug

To install JDK8, see https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-on-ubuntu-18-04#installing-specific-versions-of-openjdk 

If your server is installed with multiple versions of JDK, you must switch to JDK8. See 
https://askubuntu.com/questions/740757/switch-between-multiple-java-versions

### Install ZooKeeper

By default ZooKeeper is available in Ubuntu default repository.

Simply run the command:

$ sudo apt-get install zookeeperd

Then ZooKeeper will be started as a daemon automatically.

By default, ZooKeeper will run on port 2181.

You can run

$ netstat -ant | grep :2181 

to check on it.

### Install Kafka server

Download Kafka binaries:

curl "http://www-eu.apache.org/dist/kafka/1.1.0/kafka_2.12-1.1.0.tgz" -o ~/Downloads/kafka.tgz
or http://www.apache.org/closer.cgi?path=/kafka/0.9.0.0/

$sudo mkdir /opt/kafka

Copy the downloaded Kafka binaries to the directory /opt/kafka:

$ sudo cp kafka.tgz /opt/kafka

or 

$ sudo cp kafka_2.11-0.9.0.0.tgz /opt/kafka

$ cd /opt/kafka

$ sudo tar -xvf kafka.tgz

or 

$ sudo tar -xvf kafka_2.11-0.9.0.0.tgz

$ cd kafka_*

### Configure Kafka server

If your Kafka clients (producers and consumers) will run on the same Ubuntu host machine, you don't need to anything here.

If your Kafka clients will reside in separate servers or laptops (Linux/Mac/Windows), you must configure the Kafka servers so that *the brokers are accessible from within the same network by the producers and consumers*.

To do this, sudo open the configuration file /config/server.properties, then define the parameter "advertised.listeners":
```
# Hostname and port the broker will advertise to producers and consumers. If not set,
# it uses the value for "listeners" if configured.  Otherwise, it will use the value
# returned from java.net.InetAddress.getCanonicalHostName().
advertised.listeners=PLAINTEXT://x.y.z.w:9092
```
where x.y.z.w is the Kafka server host's IPv4 address, for example, 10.0.0.5. It is *important* that the bootstrap_servers will be x.y.z.w:9092 (e.g., 10.0.0.5:9092) when creating producers and consumers.

For Kafka version 2.11-0.9.0.0, set the parameter "advertised.host.name" to the server's IPv4 address, e.g.
```
advertised.host.name = 10.0.0.5
```

### Start Kafka server

The You can start the Kafka broker:

$ sudo bin/kafka-server-start.sh config/server.properties

You can run

$ netstat --ant | grep :9092

to check if the Kafka server is on.

### Stop Kafka server

$ sudo bin/kafka-server-stop.sh config/server.properties

## Install kafka-python at the client side

Ceate virtual environment (optioal)

$ pip install kafka-python

### Launch Kafka producer

Before starting the Kafka producer "json-producder.py", if you use a remote Kafka server in the same network, comment out the line 
```
brokers = ['0.0.0.0:9092']
```
and uncomment the line 
```
#brokers = ['10.0.0.5:9092']
```
and replace the example address "10.0.0.5" with the correct Kafka server's IPv4 address.

You can also change the topic:
```
# Assign a topic
topic = 'my-json-topic'
```

Then you can start a new terminal and run the command "python json-producer.py" to kick off. You can start multiple producers from the same machine or different machines.

### Launch Kafka consumer

Before starting the Kafka consumer "json-consumer.py", if you use a remote Kafka server in the same network, comment out the line 
```
brokers = ['0.0.0.0:9092']
```
and uncomment the line 
```
#brokers = ['10.0.0.5:9092']
```
and replace the example address "10.0.0.5" with the correct Kafka server's IPv4 address.

Make sure that the consumer will be consuming the correct topic:
```
topic = 'my-json-topic'
```
Then you can start a new terminal and run the command "python json-consumer.py". You are allowed to start multiple consumers from the same machine or different machines, but only *one* of the consumers is able to receive messages because there is only 1 partition per topic in our default configuration.

In order for multiple consumers to listen on the same topic, you can set the consumers to different groups by setting different group_id. For example, in consumer 1, you can set *group_id* to view1: 
```
topic = 'my-json-topic'
consumer = KafkaConsumer(topic, group_id='view1', bootstrap_servers=brokers)
```
In consumer 2, *group_id* can be set to view2:
```
topic = 'my-json-topic'
consumer = KafkaConsumer(topic, group_id='view2', bootstrap_servers=brokers)
```

### JavaScript Kafka Consumer

A Kafka consumer can be also created in JavaScript. See https://scotch.io/tutorials/an-introduction-to-apache-kafka.

You need to install node.js if it is not available. Refresh your local package index by typing: 
```
$ sudo apt update
```
Install Node.js from the repositories:
```
$ sudo apt install nodejs
```
Then install no-kafka that is Apache Kafka client for Node.js with new unified consumer API support (https://github.com/heroku/no-kafka#simpleconsumer). In most cases, you'll also need to install npm, the Node.js package manager:
```
$ sudo apt install npm

```
Now install no-kafka
```
$ npm install no-kafka
```
Before starting the Kafka consumer "json-consumer.js", if you use a remote Kafka server in the same network, comment out the line 
```
var brokers = '0.0.0.0:9092'
```
and uncomment the line 
```
#var brokers = '10.0.0.5:9092'
```
and replace the example address "10.0.0.5" with the correct Kafka server's IPv4 address.

Make sure that the consumer will be consuming the correct topic:
```
var topic = 'my-json-topic'
```
In order for multiple consumers to listen on the same topic, you can set the consumers to different groups by setting different *groupId*. For example:
```
const consumer = new Kafka.SimpleConsumer ({connectionString: broker, groupId: view1})
```
You can start JavaScript Kafka consumer by typing:
```
$ node json_consumer.js
```
## Use case 1: Stream video

https://scotch.io/tutorials/build-a-distributed-streaming-system-with-apache-kafka-and-python

*Note*: We must use low-resolution video source to avoid exceeding the maximum message size
