from lxml import etree as ET
from findSwitchInt import lSwitchInt
from configQueue import lConfigQueue

def lCentralMain(lEvent):
	lRoot = ET.fromstring(lEvent)
	
	#What triggered the Event? Start/Ended/Update
	lEventTrigger = lRoot[1].text

	#What type of Event is this? audio/desktopsharing
	lEventType = lRoot[0].text

	#Identify the endpoints and the port numbers and put them in a string	
	lSip1 = lRoot[2].text 
	lSport1 = lRoot[3].text 
	lSip2 = lRoot[4].text 	
	lSport2 = lRoot[5].text
	
	if lEventType == "audio":
		if lEventTrigger == "Start" or lEventTrigger == "Update":
			audioStart(lSip1, lSport1) 
			audioStart(lSip2, lSport2)
		if lEventTrigger == "Ended":
			audioEnd(lSip1, lSport1)
			audioEnd(lSip2, lSport2)






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

# Test code only. Remove before prod

lCentralMain("<EVENT><TYPE>audio</TYPE><TRIGGER>Start</TRIGGER><IP1>10.105.5.113</IP1><PORT1>382</PORT1><IP2>10.105.5.114</IP2><PORT2>568</PORT2></EVENT>")

#lCentralMain("<EVENT><TYPE>audio</TYPE><TRIGGER>Ended</TRIGGER><IP1>10.105.5.113</IP1><PORT1>382</PORT1><IP2>10.105.5.114</IP2><PORT2>568</PORT2></EVENT>")
	


