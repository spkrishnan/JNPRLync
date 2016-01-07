#!/usr/bin/env python
#This script takes switch name, switch interface, IP address and udp port information 
#Puts this information in the Config processing queue



import pika
from lxml import etree as ET

def lConfigQueue(lAction, lSwitch, lInt, lSip, lSport):
        lEqueue = "<CONFIG><ACTION>" + lAction + "</ACTION><SWITCH>" + lSwitch + "</SWITCH><INT>" + lInt + "</INT><IP>" + lSip + "</IP><PORT>" + lSport + "</PORT></CONFIG>"	
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()
	channel.queue_declare(queue='configQ1')
	channel.basic_publish(exchange='',routing_key='configQ1',body=lEqueue)
	connection.close()

# test code. remove before prod
#lConfigQueue("Add","10.105.5.216", "ge-0/0/10", "10.105.5.214", "30456")
