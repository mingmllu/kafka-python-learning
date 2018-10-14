Purpose: Gain experience with Kafka

## Install Apache ZooKeeper and Kafka servers
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

$sudo apt-get install zookeeperd

Then ZooKeeper will be started as a daemon automatically.

By default, ZooKeeper will run on port 2181.

You can run

$netstat -ant | grep :2181 

to check on it.

### Install Kafka server
Download Kafka binaries:

curl "http://www-eu.apache.org/dist/kafka/1.1.0/kafka_2.12-1.1.0.tgz" -o ~/Downloads/kafka.tgz
or http://www.apache.org/closer.cgi?path=/kafka/0.9.0.0/

$sudo mkdir /opt/kafka

Copy the downloaded Kafka binaries to the directory /opt/kafka:

$sudo cp kafka.tgz /opt/kafka

or 

$sudo cp kafka_2.11-0.9.0.0.tgz /opt/kafka

$cd /opt/kafka

$sudo tar -xvf kafka.tgz

or 

$sudo tar -xvf kafka_2.11-0.9.0.0.tgz

$cd kafka_*

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

### Start Kafka server
The You can start the Kafka broker:

$sudo bin/kafka-server-start.sh config/server.properties

You can run

$netstat --ant | grep :9092

to check if the Kafka server is on.

### Stop Kafka server
$sudo bin/kafka-server-stop.sh config/server.properties

## Install kafka-python at the client side
Ceate virtual environment (optioal)

$pip install kafka-python

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

Then you can start a new terminal and run the command "python json-consumer.py". You are allowed to start multiple consumers from the same machine or different machines, but only *one* of the consumers is able to receive messages because there is only 1 partition per topic in our default configuration.

## Use case 1: Stream video
https://scotch.io/tutorials/build-a-distributed-streaming-system-with-apache-kafka-and-python

*Note*: We must use low-resolution video source to avoid exceeding the maximum message size