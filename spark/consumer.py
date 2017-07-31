from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.mqtt import MQTTUtils

sc = SparkContext()
ssc = StreamingContext(sc, 10)

mqttStream = MQTTUtils.createStream(
    ssc, 
    "tcp://172.16.207.183:1883",  # Note both port number and protocol
    "qunews/users/mac"                  # The same routing key as used by producer
)
#mqttStream.count().pprint()
mqttStream.pprint()
ssc.start()
ssc.awaitTermination()
ssc.stop()
