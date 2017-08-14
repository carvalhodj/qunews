import pika

credentials = pika.PlainCredentials('qunews', 'qunews')
connection = pika.BlockingConnection(pika.ConnectionParameters(
               '172.16.188.133', 5672, 'qunews_host', credentials))

channel = connection.channel()

channel.exchange_declare(exchange='qunews.data',
                         type='topic',
                         durable=True)

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue


channel.queue_bind(exchange='qunews.data',
                    queue=queue_name,
                    routing_key='qunews.frequencia.ceagri')

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    texto = body.decode()
    print(texto)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
