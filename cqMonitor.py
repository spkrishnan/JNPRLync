#This script will run continuously
#Check the config queue for messages every 60 seconds
#Push the configurations to the switches

import time, threading
from qReceive import qReceive
from lxml import etree as ET
from pushConfig import lPushConfig
from datetime import datetime
from twisted.internet.task import LoopingCall
from twisted.internet import reactor




def lCqmonitor():
	lConfigList = qReceive("localhost","configQ1")
	print "\n"
	print datetime.now()	
	if lConfigList == None:
		print "Config queue empty"
		print "Waiting for messages in Config Queue..."	
		return None
	else:
		print "Config Received from Config Queue:\n"	
		print lConfigList
        lCtree = ET.fromstring(lConfigList)
	#This loop groups all configurations related to one switch
	#Calls the function that pushes the config to the switch
	for lConfigO in lCtree.findall('CONFIG'):
		lSwitchO = lConfigO.find('SWITCH').text
		lSwitchConfig = ET.fromstring("<JOB></JOB>")
		for lConfigI in lCtree.findall('CONFIG'):
			if lSwitchO == lConfigI.find('SWITCH').text:
				lSwitchConfig.append(lConfigI)
		if lSwitchConfig.findall('CONFIG') == []:
			continue
		lPushConfig(ET.tostring(lSwitchConfig, pretty_print=False))
	print "Waiting for messages in Config Queue..."



#This section of code calls the lCqmonitor function every 60 seconds
lCqmcall = LoopingCall(lCqmonitor)
lCqmcall.start(60)
reactor.run()


#Test code. Remove in prod
#ConfigList = "<JOB><CONFIG><ACTION>Add</ACTION><SWITCH>10.105.5.216</SWITCH><INT>ge-0/0/13</INT><IP>10.105.5.214</IP><PORT>30456</PORT></CONFIG><CONFIG><ACTION>Del</ACTION><SWITCH>10.105.5.217</SWITCH><INT>ge-0/0/14</INT><IP>10.105.5.214</IP><PORT>30456</PORT></CONFIG><CONFIG><ACTION>Add</ACTION><SWITCH>10.105.5.216</SWITCH><INT>ge-0/0/10</INT><IP>10.105.5.213</IP><PORT>30456</PORT></CONFIG></JOB>"

