from lxml import etree as ET
from ljunlib import audioStart
from ljunlib import audioEnd

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





