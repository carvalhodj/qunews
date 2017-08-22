from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.mqtt import MQTTUtils
import pika
import sys
import psycopg2
import os


dsn_database = "qunewdatabase"            
dsn_hostname = "localhost" 
dsn_port = "5432"               
dsn_uid = "postgres"       
dsn_pwd = "1234"      



sc = SparkContext()
ssc = StreamingContext(sc, 60)

contador = 0

IP_RABBIT = "192.168.0.102"
MQTT_PORT = "1883"

mqttStream = MQTTUtils.createStream(
    ssc, 
    "tcp://"+IP_RABBIT+':'+MQTT_PORT,  # Note both port number and protocol
    "qunews/coletor/ceagri"                  # The same routing key as used by producer
)

def ConsultarBanco(mac):
	try:
		conn_string = "host="+dsn_hostname+" port="+dsn_port+" dbname="+dsn_database+" user="+dsn_uid+" password="+dsn_pwd
		print ("Connecting to database\n  ->%s" % (conn_string))
		conn=psycopg2.connect(conn_string)
		print ("Connected!\n")
	except:
		print ("Unable to connect to the database.")
	cursor = conn.cursor()
	cursor.execute("""SELECT tt.nome from tipo_pessoamac tpm inner join tipo_pessoa tp on tpm.pessoa_fk_id = tp.id inner join tipo_tipo tt on tp.tiporef_id = tt.id where tpm.mac = """+ "'"+mac+"'")
	resultado = cursor.fetchall()
	print("Resultado consulta "+str(resultado))
	return resultado

def mapearTipo(macs):

	result = ConsultarBanco(macs)
	if (len(result) != 0):
		print("MAC "+result[0][0]+" é cadastrado")
		return (result[0][0],1)
	else:
	
		global contador
		if contador == 0:
			contador += 1
			return ('Aluno', 1)
		else:
			contador = 0
			return ('Professor', 1)

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

counts = mqttStream.flatMap(lambda mac: mac.split(','))\
                   .map(mapearTipo)\
		   .reduceByKey(lambda a, b: a + b)\
		   .map(lambda a: ('tipo', a))\
		   .groupByKey()\
		   .mapValues(list)\
		   .map(envia)


counts.pprint()
ssc.start()
ssc.awaitTermination()
ssc.stop()
