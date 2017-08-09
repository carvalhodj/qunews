from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.mqtt import MQTTUtils

sc = SparkContext()
ssc = StreamingContext(sc, 10)

contador = 0

mqttStream = MQTTUtils.createStream(
    ssc, 
    "tcp://172.16.207.183:1883",  # Note both port number and protocol
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


#mqttStream.pprint()
counts = mqttStream.flatMap(lambda mac: mac.split(','))\
                   .map(mapearTipo)\
		   .reduceByKey(lambda a, b: a + b)
counts.pprint()
ssc.start()
ssc.awaitTermination()
ssc.stop()
