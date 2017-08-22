import pika
import sys
import psycopg2
import os
import time
import datetime

IP_RABBIT = sys.argv[1]
SERIAL = "000000"

dsn_database = "qunewdatabase"            
dsn_hostname = "localhost" 
dsn_port = "5432"               
dsn_uid = "postgres"       
dsn_pwd = "1234"      

try:
	conn_string = "host="+dsn_hostname+" port="+dsn_port+" dbname="+dsn_database+" user="+dsn_uid+" password="+dsn_pwd
	print ("Connecting to database\n  ->%s" % (conn_string))
	conn=psycopg2.connect(conn_string)
	print ("Connected!\n")
except:
	print ("Unable to connect to the database.")


credentials = pika.PlainCredentials('qunews', 'qunews')
connection = pika.BlockingConnection(pika.ConnectionParameters(
               IP_RABBIT, 5672, 'qunews_host', credentials))

channel = connection.channel()

channel.exchange_declare(exchange='qunews.data',
                         type='topic',
                         durable=True)

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue


channel.queue_bind(exchange='qunews.data',
                    queue=queue_name,
                    routing_key='qunews.historico.coletor.ceagri')

print(' [*] Waiting for logs. To exit press CTRL+C')


def inserirBanco(serial,mac):
	cursor = conn.cursor()
	cursor.execute("""SELECT tp.owner_id from tipo_pessoamac tpm inner join tipo_pessoa tp on tpm.pessoa_fk_id = tp.id where tpm.mac = \'"""+ mac+"\'")
	iduser = cursor.fetchall()
	print(iduser)

	print(len(iduser))

	if (len(iduser) != 0):
		print(iduser[0][0])
		idu = iduser[0][0]
		cursor.execute("""select id from tipo_local where serial = \'"""+ serial+"\'")
		retserial = cursor.fetchall()
		if (len(retserial) != 0):
			idlocal = retserial[0][0]
		
			timestamp = PegarTimeStamp()
			print(idlocal)
			cursor.execute("""insert into tipo_historico (created, local_ref_id, user_ref_id) values """+"(\'"+str(timestamp)+"\'"+","+str(idlocal)+","+str(idu)+")")
			conn.commit()
		else:
			print("Serial não existe")
	else:
		print("Endereço mac não cadastrado")

def PegarTimeStamp():
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	return st






def callback(ch, method, properties, body):
	global headers
	global SERIAL
	texto = body.decode()
	print(texto)
	lista = texto.split(":")
	if lista[0] != '':
		if "," in lista[0]:
			lmac = lista[0].split(",")
			print(lmac)
			for i in lmac:
				inserirBanco(lista[1],i)
				

		else:
			inserirBanco(lista[1],lista[0])
			print("Só tem 1 mac")
	else:
		print("Não tem mac")
				

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()



"9c99a0d1bb70, 103b59b33bca:0891dfb5"
