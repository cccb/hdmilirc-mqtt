import network
import time

class Wifi(object):
	nic = None
	essid = None
	password= None

	def __init__(self, ssid, password, ifconfig=None):
		self.nic = network.WLAN(network.STA_IF)
		self.nic.active(True)
		self.essid = ssid
		self.password = password
		if ifconfig:
			self.nic.ifconfig(tuple(ifconfig))

	def connect(self):
		if self.nic.isconnected():
			return True
		self.nic.connect(self.essid, self.password)
		retries = 0
		while not self.nic.isconnected:
			time.sleep_ms(500)
			retries += 1

			if retries > 20:
				return False
		return True
