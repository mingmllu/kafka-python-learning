# json-producer.py

import time
import json
from kafka import KafkaProducer
import random

#  connect to Kafka
KAFKA_VERSION = (0, 10)
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
# Assign a topic
topic = 'my-json-topic'
location = 'Kiosk_A'

def json_emitter():

    print(' emitting.....')
    for i in range(1000):
        # Send to kafka
        print("Message %d sent =====> " % i)
        u = dict(camera = location, count_person = random.randint(0, 4))
        producer.send(topic, u)
        # To reduce CPU usage create sleep time of 0.02sec  
        time.sleep(0.2)
    print('done emitting')

if __name__ == '__main__':
    json_emitter()