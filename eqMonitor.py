#This script will run continuously
#Check the event queue for messages every 30 seconds
#Calls the Central processing function to process the event

import time, threading
from ljunlib import qReceive
from lxml import etree as ET
from datetime import datetime
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from central import lCentralMain


def lEqmonitor():
	lEventList = qReceive("localhost","eventQ1")
	print "\n"
	print datetime.now()	
	if lEventList == None:
		print "Event queue empty"
		return None
	else:
		print "Events Received from Event Queue:\n"	
        
	lEtree = ET.fromstring(lEventList)
	for lEvent in lEtree.findall('EVENT'):
		print "\nThis event is being processed:"	
		print ET.tostring(lEvent, pretty_print=True)
		lCentralMain(ET.tostring(lEvent, pretty_print=False))	
 



#This section of code calls the lEqmonitor function every 30 seconds
lEqmcall = LoopingCall(lEqmonitor)
lEqmcall.start(30)
reactor.run()


