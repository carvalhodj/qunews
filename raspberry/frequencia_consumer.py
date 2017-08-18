import pika

credentials = pika.PlainCredentials('qunews', 'qunews')
connection = pika.BlockingConnection(pika.ConnectionParameters(
               '10.0.0.17', 5672, 'qunews_host', credentials))

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

def calcula_total_macs(macs):
    total = 0
    
    for tipo in macs:
        total += int(tipo[1])
    
    return total


def calcula_frequencias(lista_macs):
    total_macs = calcula_total_macs(lista_macs)
    lista_frequencias = []

    for tipo in lista_macs:
        frequencia_relativa = float(tipo[1])/total_macs
        frequencia_relativa_rounded = round(frequencia_relativa, 2)
        lista_frequencias.append((tipo[0], frequencia_relativa_rounded))

    return lista_frequencias


def callback(ch, method, properties, body):
    texto = body.decode()
    lista = calcula_frequencias(eval(texto))
    print(lista)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
