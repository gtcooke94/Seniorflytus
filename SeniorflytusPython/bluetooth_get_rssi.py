from bluepy.btle import Scanner, DefaultDelegate
import time

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            pass #print "Discovered device", dev.addr
        elif isNewData:
            pass #print "Received new data from", dev.addr

#
def get_rssi(pebble_mac = "0e:0a:a0:01:4b:ca"):
	scanner = Scanner().withDelegate(ScanDelegate())
	devices = scanner.scan(1.1)
	for dev in devices:
		if dev.addr == pebble_mac:
			pebble = dev
			return pebble.rssi
		else:
			pass
	
try:	
	while 1:
		print get_rssi()	
except:
	KeyboardInterrupt
	TxPower = raw_input('-->')
	print "TxPower:" + str(TxPower) 
