#!/usr/bin/env python

#Takes Server and Queue name as input
#returns all the messages in the queue
#Closes the connection after the queue is empty

import pika
lQConfig = ""

class CountCallback(object):
    def __init__(self, count):
        self.count = count
	self.config = "<JOB>"

    def __call__(self, ch, method, properties, body):
	global lQConfig
	self.config = self.config + body	
	ch.basic_ack(delivery_tag = method.delivery_tag)	
	self.count -= 1
        if self.count < 1:
            ch.stop_consuming()
	    self.config = self.config + "</JOB>"
	    lQConfig = self.config

def qReceive(lServer,lQueue):
	global lQConfig
	connection = pika.BlockingConnection(pika.ConnectionParameters(host=lServer))
	channel = connection.channel()
	queue = channel.queue_declare(lQueue)
	if queue.method.message_count == 0:
		connection.close()
		return None	
	callback = CountCallback(queue.method.message_count)
	channel.basic_consume(callback, queue=lQueue)
	channel.start_consuming()
	CountCallback(queue.method.message_count)
	connection.close()
	return lQConfig


#qReceive("localhost","configQ1")
