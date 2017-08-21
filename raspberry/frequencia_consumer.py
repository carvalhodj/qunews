import pika
import sys
import requests, json
import urllib.request
from get_serial import get_serial

IP_RABBIT = sys.argv[1]
IP_REST = "http://" + sys.argv[2] + ":8000/teste/"
SERIAL = "000000"

headers = {'Content-type': 'application/json'}

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
        lista_frequencias.append((tipo[0], int(frequencia_relativa_rounded*10)))

    return lista_frequencias


def callback(ch, method, properties, body):
    global headers
    global IP_REST
    global SERIAL
    texto = body.decode()
    lista = calcula_frequencias(eval(texto))
    print("Frequências: {}".format(lista))
    lista_formatada = []
    for tupla in lista:
        nova_tupla = (tupla[0],tupla[1])
        lista_formatada.append(nova_tupla)
    msg ='\"'+SERIAL+';'+str(lista_formatada)+'\"'
    noticias = requests.post(IP_REST, data=msg, headers=headers)
    dados = noticias.json()
    nome_cont = 1
    for item in dados:
        link = "http://192.168.0.104:8000"+item['image']
        nome_arq = ""
        if nome_cont < 10:
            nome_arq += '00' + str(nome_cont) + '.png'
        else:
            nome_arq += '0' + str(nome_cont) + '.png'
        nome_cont += 1
        urllib.request.urlretrieve(link, nome_arq)
    print("Oie!")

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
