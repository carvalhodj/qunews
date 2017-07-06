import pika
import sys

credentials = pika.PlainCredentials('qunews', 'qunews')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, 'qunews_host', credentials))
channel    = connection.channel()

channel.exchange_declare(exchange='qunews_data', type='topic')

routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
message     = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(exchange='qunews_data', routing_key=routing_key, body=message)

print("[x] Sent %r:%r" % (routing_key, message))
connection.close()

