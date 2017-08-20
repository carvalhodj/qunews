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
