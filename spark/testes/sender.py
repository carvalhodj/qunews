import pika

cred = pika.PlainCredentials('qunews', 'qunews')
conn = pika.BlockingConnection(pika.ConnectionParameters('172.16.207.183', 5672, 'qunews_host', cred))

channel = conn.channel()

channel.exchange_declare(exchange='qunews.data',
			 type='topic', durable=True)
x = [('a', 10), ('b', 20), ('c', 30)]

channel.basic_publish(
	exchange='qunews.data',
	routing_key='qunews.frequencia.ceagri',
	body=str(x)
)
print("Sent {}".format(str(x)))
conn.close()
