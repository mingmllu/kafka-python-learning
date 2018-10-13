from kafka import KafkaConsumer
#connect to Kafka server and pass the topic we want to consume
consumer = KafkaConsumer('my-json-topic', group_id='view', bootstrap_servers=['0.0.0.0:9092'])

for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))