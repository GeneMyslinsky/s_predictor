from confluent_kafka import Producer
import json
import socket
import uuid
# v = {'request_type':"hist",'contract':{'type':'STOCK','symbol':'SPY','exchange':'SMART','currency':'USD'},'params':{'endt':'20201005 23:99','dur':'3 D','candles':'15 secs','show':'TRADES'}}
k_conn = {'bootstrap.servers': "broker:29092",
        'client.id': socket.gethostname()}
producer = Producer(k_conn)

def ProduceJ(topic,value):
    producer.produce(topic, key=str(uuid.uuid4()), value=json.dumps(value))

def ProduceB(topic,key, value):
    producer.produce(topic, key=json.dumps(key), value=value)