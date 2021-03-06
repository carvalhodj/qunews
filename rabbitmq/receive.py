import pika
import sys

credentials = pika.PlainCredentials('qunews', 'qunews')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, 'qunews_host', credentials))
channel = connection.channel()

channel.exchange_declare(exchange='qunews_data',
                         type='topic')

result = channel.queue_declare()
queue_name = result.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(exchange='qunews_data',
                       queue=queue_name,
                       routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))
    if body[0:2] == 'ef':
        print("MAC comeca com 'ef'")

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
