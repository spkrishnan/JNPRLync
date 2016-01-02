import yaml


def lSwitchInt(lSip):
	with open('maclist.yml', 'r') as fsp:
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
lSwitchInt("10.105.5.214")
