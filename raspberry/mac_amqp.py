import pcap, dpkt, binascii
import pika
import sys
import threading
from get_serial import get_serial

MACS = {}
TIME_OUT = 10

mensagem = ""

SERIAL = get_serial()

end_ip = sys.argv[1:]

if not end_ip:
    print >> sys.stderr, "Fomato: %s [SERVER IP ADDRESS]" % (sys.argv[0])

credentials = pika.PlainCredentials('qunews', 'qunews')
connection = pika.BlockingConnection(pika.ConnectionParameters(sys.argv[1], 5672, 'qunews_host', credentials))
channel = connection.channel()

channel.exchange_declare(exchange='qunews.data', type='topic', durable=True)

routing_key = 'qunews.coletor.ceagri'
historico_routing_key = 'qunews.historico.coletor.ceagri'

"""
## Inicio do codigo de callback
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='qunews.data',
                   queue=queue_name,
                   routing_key='qunews.frequencia.ceagri')

def callback(ch, method, properties, body):
    try:
        body = eval(body)
        freq1, freq2, freq3 = body[0], body[1], body[2] # considerando que a mensagem sera uma lista de tuplas
        print(freq1)
        print(freq2)
        print(freq3)
    except:
        print("Erro no recebimento das tuplas")

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)
#channel.start_consuming()
## Fim do codigo de callback
"""

def enviaAMQP(rk, hrk):
    global mensagem
    global SERIAL
#    global SERIAL
#    print(SERIAL)
    channel.basic_publish(exchange='qunews.data', routing_key=rk, body=mensagem)
    channel.basic_publish(exchange='qunews.data', routing_key=hrk, body=mensagem+':'+SERIAL)
    threading.Timer(10, enviaAMQP, [rk,hrk]).start()

enviaAMQP(routing_key, historico_routing_key)

for ts, pkt in pcap.pcap(name='wlan0'):
    try:
        rtap = dpkt.radiotap.Radiotap(pkt)
    except:
        pass
    wifi = rtap.data
    if wifi.type == 0 and wifi.subtype == 4:
        mac = binascii.hexlify(wifi.mgmt.src)
        ssid = wifi.ies[0].info
        MACS[mac] = ts
        for mac in list(MACS):
            if(ts - MACS[mac] >= TIME_OUT):
                del MACS[mac]
        print("### TAMANHO DICIONARIO = %d" % len(MACS))
        mensagem = str(list(MACS.keys())).replace('[', '').replace(']', '').replace('\'', '')
