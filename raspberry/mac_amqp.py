import pcap, dpkt, binascii
import pika

credentials = pika.PlainCredentials('qunews', 'qunews')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.107', 5672, 'qunews_host', credentials))
channel = connection.channel()

channel.exchange_declare(exchange='qunews_data', type='topic')

routing_key = 'qunews.user.mac'

def enviaAMQP(rk, msg):
    return channel.basic_publish(exchange='qunews_data', routing_key=rk, body=msg)

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
        #print(ts, src, ssid)
        #print("\n")
