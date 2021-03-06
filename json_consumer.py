from kafka import KafkaConsumer

# If the broker installed on a separate host machine,
# use the machine's IP address
#brokers = ['10.0.0.5:9092']
# If the broker installed on the same host machine, use localhost or 0.0.0.0
brokers = ['0.0.0.0:9092']

#connect to Kafka server and pass the topic we want to consume
topic = 'my-json-topic'
consumer = KafkaConsumer(topic, group_id='view', bootstrap_servers=brokers)
print("Start to listen on Kafka broker")
print("It may take some time to receive the first message")
print("")

for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))