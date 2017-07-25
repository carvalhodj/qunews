import pcap, dpkt, binascii
import pika

#connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.0.108'))

credentials = pika.PlainCredentials('qunews', 'qunews')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.108', 5672, 'qunews_host', credentials))
channel = connection.channel()

channel.exchange_declare(exchange='qunews.data', type='topic', durable=True)

routing_key = 'qunews'

def enviaAMQP(rk, msg):
    return channel.basic_publish(exchange='qunews.data', routing_key=rk, body=msg)

for ts, pkt in pcap.pcap(name='wlan0'):
    try:
        rtap = dpkt.radiotap.Radiotap(pkt)
    except:
        pass
    wifi = rtap.data
    if wifi.type == 0 and wifi.subtype == 4:
        src = binascii.hexlify(wifi.mgmt.src)
        ssid = wifi.ies[0].info
        enviaAMQP(routing_key, src)   
        print(ts, src, ssid)
        print("\n")
