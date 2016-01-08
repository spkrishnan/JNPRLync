import pika
from lxml import etree as ET
import yaml
from jinja2 import Template
import logging
import sys
import time
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from logging import *


def audioStart(lSip, lSport):
	lSipSport = lSip + ":" + lSport	
	lExist = lCheckList(lSipSport)
	if lExist != True:
		lSwitch, lSint = lSwitchInt(lSip) 
		if lSwitch != "None":
			lConfigQueue("Add",lSwitch,lSint,lSip,lSport)
			lAddList(lSipSport)	
		else:
			print "Config addition failed. Could not locate switch for " + lSip
	else:
		print "Audio already improved for " + lSipSport






def audioEnd(lSip, lSport):
	lSipSport = lSip + ":" + lSport
	lExist = lCheckList(lSipSport)
	if lExist == True:
		lSwitch, lSint = lSwitchInt(lSip)
                
		if lSwitch != "None":
                        lConfigQueue("Del",lSwitch,lSint,lSip,lSport)
                	lRemList(lSipSport)
                	print "End Audio for " + lSipSport	
                else:
                        print "Config Deletion failed. Could not locate switch for " + lSip

	else:
		print "No Audio call found for " + lSipSport


def lAddList(lSipSport):
        #Get the parameter and add new line
        lSipSportV = lSipSport + "\n"

        #Read the file into a list
        lFlist = list()
        lF = open("lEventFile", "r+")
        lFlist = lF.readlines()

        #Add entry to the list
        lFlist.extend(lSipSportV)

        #Save the new list into the file
        lF.seek(0)
        lF.truncate()
        for item in lFlist:
                lF.write(item)
        lF.close()

def lCheckList(lSipSport):
        #Get the parameter and add new line
        lSipSportV = lSipSport + "\n"

        #Read the file into a list
        lFlist = list()
        lF = open("lEventFile", "r+")
        lFlist = lF.readlines()

        #Check if this entry is already in the list
        if lSipSportV in lFlist:
                return True
        lF.close()


def lRemList(lSipSport):
        #Get the parameter and add new line
        lSipSportV = lSipSport + "\n"

        #Read the file into a list
        lFlist = list()
        lF = open("lEventFile", "r+")
        lFlist = lF.readlines()

        #Remove entry from the list
        lFlist.remove(lSipSportV)

        #Save the new list into the file
        lF.seek(0)
        lF.truncate()
        for item in lFlist:
                lF.write(item)
        lF.close()


#This function takes switch name, switch interface, IP address and udp port information 
#Puts this information in the Config processing queue
def lConfigQueue(lAction, lSwitch, lInt, lSip, lSport):
        lEqueue = "<CONFIG><ACTION>" + lAction + "</ACTION><SWITCH>" + lSwitch + "</SWITCH><INT>" + lInt + "</INT><IP>" + lSip + "</IP><PORT>" + lSport + "</PORT></CONFIG>"
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='configQ1')
        channel.basic_publish(exchange='',routing_key='configQ1',body=lEqueue)
        connection.close()



def lSwitchInt(lSip):
        with open('lMaclist.yml', 'r') as fsp:
                fspd = yaml.load(fsp)
        fspt = fspd.get(lSip)
        if fspt != None:
                lSwitch = fspt.get("switch")
                lInt = fspt.get("int")
                fsp.close()
                return (lSwitch, lInt)
        else:
                fsp.close()
                return ("None", "None")



#This function takes an xml string as input
#Parses the XML data and queues them in the Event Queue
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





#This function can only configure one switch at a time
#Pushes the configuration to the switch
#Commits the configuration
#This function takes xml variable as input
#Example xml input: 
#<JOB><CONFIG><ACTION>Add</ACTION><SWITCH>10.105.5.216</SWITCH><INT>ge-0/0/13</INT><IP>10.105.5.214</IP><PORT>30456</PORT></CONFIG><CONFIG><ACTION>Del</ACTION><SWITCH>10.105.5.216</SWITCH><INT>ge-0/0/14</INT><IP>10.105.5.214</IP><PORT>30456</PORT></CONFIG></CONFIG></JOB>
def lPushConfig(lConfigList):
	with open('lAddTemplate.j2') as lTA_fh:
		lTAdd_format = lTA_fh.read()


	with open('lDelTemplate.j2') as lTD_fh:
                lTDel_format = lTD_fh.read()

	# This section is for logging
	lLgr = logging.getLogger('lync_pushconfig')
	lLgr.setLevel(logging.INFO)

	lLog_fh = logging.FileHandler('lync_pushconfig.log')
	lLog_fh.setLevel(logging.INFO)

	lFrmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	lLog_fh.setFormatter(lFrmt)
	lLgr.addHandler(lLog_fh)


	#Prepare the configuration that needs to be pushed to this switch
	lTempData = {}
	lAddTemplate = Template(lTAdd_format)
	lDelTemplate = Template(lTDel_format)
	
	lClistRoot = ET.fromstring(lConfigList)	

        lSwitch = Device(host=lClistRoot[0][1].text,user='root',password='testing123')
        
	#Open connection to the switch
        lSwitch.open()
        lSwitchConf = Config(lSwitch)


	lLgr.info("\n\n\n\n")
        lLgr.info(lSwitch)

	for lConfig in lClistRoot:
		if lConfig[0].text == "Add":
			lTempData['lIP'] = lConfig[3].text
			lTempData['lPort'] = lConfig[4].text
			lTempData['lInt'] = lConfig[2].text
 			lAllConfig = lAddTemplate.render(lTempData)
			#Push config to switch
			print "\nPushing Config to " + str(lSwitch) + "\n"
			print lAllConfig + "\n\n"	
			lSwitchConf.load(lAllConfig, format='set')
			lLgr.info("\n")
        		lLgr.info(lAllConfig)
		else:
			lTempData['lIP'] = lConfig[3].text
                        lTempData['lPort'] = lConfig[4].text
                        lTempData['lInt'] = lConfig[2].text
                        lAllConfig = lDelTemplate.render(lTempData)
			#Push config to switch 
                        print "\nPushing Config to " + str(lSwitch) + "\n"
                        print lAllConfig + "\n\n" 
                        lSwitchConf.load(lAllConfig, format='set')
			lLgr.info("\n")
                        lLgr.info(lAllConfig)

			
	#Commit configuration changes	
	lSwitchConf.commit()
	

	#Close connection to the switch
	lSwitch.close()
	



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



#Takes Server and Queue name as input
#returns all the messages in the queue
#Closes the connection after the queue is empty
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

