# json-producer.py

import time
import json
from kafka import KafkaProducer
import random
import socket

# If the broker installed on a separate host machine,
# use the machine's IP address
brokers = ['10.4.17.190:9092']
# If the broker installed on the same host machine, use localhost or 0.0.0.0
#brokers = ['0.0.0.0:9092']

#  connect to Kafka
KAFKA_VERSION = (0, 10)
producer = KafkaProducer(bootstrap_servers=brokers, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
# Assign a topic
topic = 'test-delay'
location = 'Hostname:' + socket.gethostname()
bbox = [0.45153582096099854, 0.7991291880607605, 0.6119496822357178, 0.8229450583457947]
def json_emitter():

    print('emitting.....')
    i = 0
    while True:
        # Send to kafka
        print("Message %d sent =====> " % i)
        u = dict(camera = location, count_person = random.randint(0, 4), timestamp = time.time(), bbox = [])
        for _ in range(16):
            u["bbox"].append(bbox)
        m = producer.send(topic, u)
        #print(m.get())
        # To reduce CPU usage create sleep time of 0.2sec  
        time.sleep(0.02)
        i += 1
    print('done emitting')

if __name__ == '__main__':
    json_emitter()
