from kafka import KafkaConsumer
import time
import json

# If the broker installed on a separate host machine,
# use the machine's IP address
brokers = ['10.4.17.190:9092']
#brokers = ['135.222.154.160:9092']
#brokers = ['10.4.17.190:9092']
# If the broker installed on the same host machine, use localhost or 0.0.0.0
#brokers = ['0.0.0.0:9092']

#connect to Kafka server and pass the topic we want to consume
topic = 'aggregate_sti'
consumer = KafkaConsumer(topic, group_id='myview2', bootstrap_servers=brokers, auto_commit_interval_ms=100)
#consumer.seek_to_end()
print("Start to listen on Kafka broker")
print("It may take some time to receive the first message")
print("")

max_dt_from_detect_to_kafka = None
min_dt_from_detect_to_kafka = None

max_dt_from_kafka_to_consumer = None
min_dt_from_kafka_to_consumer = None

start_to_consume_time = time.time()
message_counter = 0

message_counter_max_dt_from_kafka_to_consumer = -1

message_offset = -1

time_last_message = 0

for message in consumer:
    #consumer.seek_to_end()
    print("--------> time step = %f" % (time.time() - time_last_message))
    time_last_message = time.time()
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    message_counter += 1
    #if message_counter > 10:
    #    break
    if message_counter == 1:
        continue
    s = message.value.decode("utf-8") 
    data_double_quotes = s.replace("\'", "\"") #JSON strings must use double quotes
    data_dict = json.loads(data_double_quotes)
    dt_from_detect_to_kafka = data_dict["ts2kafka"] - data_dict["detect_ts"]
    dt_from_kafka_to_consumer = time.time() - data_dict["ts2kafka"]
    
    if max_dt_from_detect_to_kafka == None:
        max_dt_from_detect_to_kafka = dt_from_detect_to_kafka
    if min_dt_from_detect_to_kafka == None:
        min_dt_from_detect_to_kafka = dt_from_detect_to_kafka
    if max_dt_from_detect_to_kafka < dt_from_detect_to_kafka:
        max_dt_from_detect_to_kafka = dt_from_detect_to_kafka
    if min_dt_from_detect_to_kafka > dt_from_detect_to_kafka:
        min_dt_from_detect_to_kafka = dt_from_detect_to_kafka

    if max_dt_from_kafka_to_consumer == None:
        max_dt_from_kafka_to_consumer = dt_from_kafka_to_consumer
        message_counter_max_dt_from_kafka_to_consumer = message_counter
    if min_dt_from_kafka_to_consumer == None:
        min_dt_from_kafka_to_consumer = dt_from_kafka_to_consumer
    if max_dt_from_kafka_to_consumer < dt_from_kafka_to_consumer:
        max_dt_from_kafka_to_consumer = dt_from_kafka_to_consumer
    
    #if max_dt_from_kafka_to_consumer > 0 :
    #    max_dt_from_kafka_to_consumer = dt_from_kafka_to_consumer
    #if dt_from_kafka_to_consumer < 0:
    #    if dt_from_kafka_to_consumer > max_dt_from_kafka_to_consumer:
    #        max_dt_from_kafka_to_consumer = dt_from_kafka_to_consumer

    if min_dt_from_kafka_to_consumer > dt_from_kafka_to_consumer:
        min_dt_from_kafka_to_consumer = dt_from_kafka_to_consumer

    if message_offset == -1:
        message_offset = message.offset
    print("Now %f ---------------- message.offset %d message offset gap: %d" % (time.time(), message.offset, message.offset - message_offset))
    message_offset = message.offset

    print("dt_from_detect_to_kafka: max %f min %f spread [%f]" % (max_dt_from_detect_to_kafka, min_dt_from_detect_to_kafka, max_dt_from_detect_to_kafka - min_dt_from_detect_to_kafka))
    print("dt_from_kafka_to_consumer: max[%d] %f min %f" % (message_counter_max_dt_from_kafka_to_consumer, max_dt_from_kafka_to_consumer, min_dt_from_kafka_to_consumer))
    print("dt_from_kafka_to_consumer: max %f min %f spread [%f]" % (max_dt_from_kafka_to_consumer, min_dt_from_kafka_to_consumer, max_dt_from_kafka_to_consumer- min_dt_from_kafka_to_consumer))

    #print("message_counter %d message_counter_max_dt_from_kafka_to_consumer %d" %(message_counter, message_counter_max_dt_from_kafka_to_consumer))

    print("Detector to Kafka: %f Kafka to Consumer: %f message_counter %d" % (dt_from_detect_to_kafka, dt_from_kafka_to_consumer, message_counter))
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))

    #if max_dt_from_kafka_to_consumer > 5:
    if time.time() - time_last_message > 5:
        print("exit %f" %(time.time()))
        break
