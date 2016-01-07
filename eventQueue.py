#!/usr/bin/env python
#This script takes an xml string as input
#Parses the XML data and queues them in the Event Queue



import pika
from lxml import etree as ET

def eventQueue(lEvent):
	lRoot = ET.fromstring(lEvent)
        lType = lRoot[1].get('Type')
        lTrigger = lRoot[1].tag
        lIp1 = lRoot[1][0].find('IP').text
        lPort1 = lRoot[1][0].find('Port').text
        lIp2 = lRoot[1][1].find('IP').text
        lPort2 = lRoot[1][1].find('Port').text
        lEqueue = "<EVENT><TYPE>" + lType + "</TYPE><TRIGGER>" + lTrigger + "</TRIGGER><IP1>" + lIp1 + "</IP1><PORT1>" + lPort1 + "</PORT1><IP2>" + lIp2 + "</IP2><PORT2>" + lPort2 + "</PORT2></EVENT>"	


	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()
	channel.queue_declare(queue='eventQ1')
	channel.basic_publish(exchange='',routing_key='eventQ1',body=lEqueue)
	connection.close()

