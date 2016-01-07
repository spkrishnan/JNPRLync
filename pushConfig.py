#This script takes xml variable as input
#Example xml input: 
#<JOB><CONFIG><ACTION>Add</ACTION><SWITCH>10.105.5.216</SWITCH><INT>ge-0/0/13</INT><IP>10.105.5.214</IP><PORT>30456</PORT></CONFIG><CONFIG><ACTION>Del</ACTION><SWITCH>10.105.5.216</SWITCH><INT>ge-0/0/14</INT><IP>10.105.5.214</IP><PORT>30456</PORT></CONFIG></CONFIG></JOB>
#This script can only configure one switch at a time
#Pushes the configuration to the switch
#Commits the configuration


import yaml
from jinja2 import Template
import logging
import sys
import time
from lxml import etree as ET
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from logging import *


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
	

#Test Configuration
#lPushConfig("<JOB><CONFIG><ACTION>Add</ACTION><SWITCH>10.105.5.216</SWITCH><INT>ge-0/0/13</INT><IP>10.105.5.214</IP><PORT>30456</PORT></CONFIG><CONFIG><ACTION>Del</ACTION><SWITCH>10.105.5.216</SWITCH><INT>ge-0/0/14</INT><IP>10.105.5.214</IP><PORT>30456</PORT></CONFIG><CONFIG><ACTION>Add</ACTION><SWITCH>10.105.5.216</SWITCH><INT>ge-0/0/10</INT><IP>10.105.5.213</IP><PORT>30456</PORT></CONFIG></JOB>")

