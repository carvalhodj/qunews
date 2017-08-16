from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.mqtt import MQTTUtils
import pika

sc = SparkContext()
ssc = StreamingContext(sc, 10)

contador = 0

IP_RABBIT = "192.168.0.11"
MQTT_PORT = "1883"

mqttStream = MQTTUtils.createStream(
    ssc, 
    "tcp://"+IP_RABBIT+':'+MQTT_PORT,  # Note both port number and protocol
    "qunews/coletor/ceagri"                  # The same routing key as used by producer
)

def mapearTipo(macs):
    global contador
    if contador == 0:
        contador += 1
        return ('aluno', 1)
    elif contador == 1:
        contador += 1
        return ('professor', 1)
    else:
        contador = 0
        return ('funcionario', 1)

def envia(frequencia):
    global IP_RABBIT
    credentials = pika.PlainCredentials('qunews', 'qunews')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
               IP_RABBIT, 5672, 'qunews_host', credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange='qunews.data',
                 type='topic', durable=True)

    channel.basic_publish(
        exchange='qunews.data',  # amq.topic as exchange
        routing_key='qunews.frequencia.ceagri',   # Routing key used by producer
        body=str(frequencia[1])
    )

    connection.close()
    return 1
"""
counts = mqttStream.flatMap(lambda mac: mac.split(','))\
                   .map(mapearTipo)\
		   .reduceByKey(lambda a, b: a + b)\
		   .map(lambda a: ('tipo', a))\
		   .groupByKey()\
		   .mapValues(list)\
		   .map(envia)
"""

lines = spark.read.text('teste.txt').rdd.map(lambda r: r[0])

counts = lines.map(lambda x: (x, 1))

total_macs = counts.count()

counts = counts.reduceByKey(lambda x, y: x + y)\
	       .map(lambda x: (x[0], float(x[1])/total_macs))

counts.pprint()
ssc.start()
ssc.awaitTermination()
ssc.stop()
