const Kafka = require('no-kafka');

// Create an instance of the Kafka consumer
// If the broker installed on a separate host machine,
// use the machine's IP address
//var broker = '10.0.0.5:9092'
// If the broker installed on the same host machine, use localhost or 0.0.0.0
var brokers = '0.0.0.0:9092'
const consumer = new Kafka.SimpleConsumer ({connectionString: broker})
var data = function (messageSet, topic, partition) {
    messageSet.forEach(function (m) {
        console.log(topic, partition, m.offset, m.message.value.toString('utf8'));
    });
};

// Subscribe to the Kafka topic
var topic = 'dogwood-topic'
return consumer.init().then(function () {
    return consumer.subscribe(topic, data);
});
