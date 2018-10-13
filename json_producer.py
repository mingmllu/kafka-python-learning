# json-producer.py

import time
import json
from kafka import KafkaProducer
#  connect to Kafka
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
# Assign a topic
topic = 'my-json-topic'

def json_emitter():

    print(' emitting.....')
    for i in range(1000):
        # Send to kafka
        print(i)
        u = dict(msg = i)
        producer.send(topic, u)
        # To reduce CPU usage create sleep time of 0.02sec  
        time.sleep(0.02)
    print('done emitting')

if __name__ == '__main__':
    json_emitter()