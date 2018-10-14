# json-producer.py

import time
import json
from kafka import KafkaProducer
import random
import socket

# If the broker installed on a separate host machine,
# use the machine's IP address
#brokers = ['10.0.0.5:9092']
# If the broker installed on the same host machine, use localhost or 0.0.0.0
brokers = ['0.0.0.0:9092']

#  connect to Kafka
KAFKA_VERSION = (0, 10)
producer = KafkaProducer(bootstrap_servers=brokers, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
# Assign a topic
topic = 'my-json-topic'
location = 'Hostname:' + socket.gethostname()

def json_emitter():

    print('emitting.....')
    i = 0
    while True:
        # Send to kafka
        print("Message %d sent =====> " % i)
        u = dict(camera = location, count_person = random.randint(0, 4))
        producer.send(topic, u)
        # To reduce CPU usage create sleep time of 0.2sec  
        time.sleep(0.2)
        i += 1
    print('done emitting')

if __name__ == '__main__':
    json_emitter()