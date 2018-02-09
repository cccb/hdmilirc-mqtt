import machine

import config
import wifi
import mqtt

def _mqtt_callback(topic, msg):
    print("MQTT cb:")
    print(topic.decode())
    print(msg.decode())


def _mqtt_connect(c):
	while True:
		try:
			print(c.connect())
			if not c.connect():
				print('New session being set up')
                topic = b'{}/#'.format(config.mqttbasetopic)
                print('Subscribe to {}'.format(topic))
                c.subscribe(topic)
				break
		except:
			pass

def main():

    # Connect to wifi
	w = Wifi(config.ssid, config.password, config.ifconfig)
	if not w.connect():
        print("Could not connect to wifi")
		machine.reset()

	time.sleep_ms(300)

	c = MQTTClient('umqtt_client', config.mqttserver, port=config.mqttport)
	c.DEBUG = True
	c.set_callback(_mqtt_callback)

    _mqtt_connect(c)

	while True:
        c.wait_msg()


try:
    main()

except:
	raise
	machine.reset()



