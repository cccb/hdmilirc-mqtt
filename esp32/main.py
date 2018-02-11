
import time
import json

import machine

import config
import wifi
import mqtt


# Actions
GET_CHANNEL_INPUTS_REQUEST = "@hdmi/GET_CHANNEL_INPUTS_REQUEST"
GET_CHANNEL_INPUTS_SUCCESS = "@hdmi/GET_CHANNEL_INPUTS_SUCCESS"

SET_CHANNEL_A_INPUT_REQUEST = "@hdmi/SET_CHANNEL_A_INPUT_REQUEST"
SET_CHANNEL_A_INPUT_START   = "@hdmi/SET_CHANNEL_A_INPUT_START"
SET_CHANNEL_A_INPUT_SUCCESS = "@hdmi/SET_CHANNEL_A_INPUT_SUCCESS"
SET_CHANNEL_A_INPUT_ERROR   = "@hdmi/SET_CHANNEL_A_INPUT_ERROR"
SET_CHANNEL_A_INPUT_CANCEL  = "@hdmi/SET_CHANNEL_A_INPUT_CANCEL"

SET_CHANNEL_B_INPUT_REQUEST = "@hdmi/SET_CHANNEL_B_INPUT_REQUEST"
SET_CHANNEL_B_INPUT_START   = "@hdmi/SET_CHANNEL_B_INPUT_START"
SET_CHANNEL_B_INPUT_SUCCESS = "@hdmi/SET_CHANNEL_B_INPUT_SUCCESS"
SET_CHANNEL_B_INPUT_ERROR   = "@hdmi/SET_CHANNEL_B_INPUT_ERROR"
SET_CHANNEL_B_INPUT_CANCEL  = "@hdmi/SET_CHANNEL_B_INPUT_CANCEL"


#
# Action creators
#
def get_channel_inputs_success():
    return {
        "type": GET_CHANNEL_INPUTS_SUCCESS,
        "payload": {
            "a": hdmi.get_selected(hdmi.STATE_A),
            "b": hdmi.get_selected(hdmi.STATE_B),
        }
    }


def set_channel_a_start(next_id):
    return {
        "type": SET_CHANNEL_A_INPUT_START,
        "payload": {
            "id": next_id,
        },
    }


def set_channel_a_success(next_id):
    return {
        "type": SET_CHANNEL_A_INPUT_SUCCESS,
        "payload": {
            "id": next_id,
        },
    }


def set_channel_a_cancel(channel_id):
    return {
        "type": SET_CHANNEL_A_INPUT_CANCEL,
        "payload": {
            "id": channel_id,
        },
    }


def set_channel_a_error(requested_id, next_id):
    return {
        "type": SET_CHANNEL_A_INPUT_ERROR,
        "payload": {
            "requested_id": requested_id,
            "id": next_id,
        },
    }


def set_channel_b_start(next_id):
    return {
        "type": SET_CHANNEL_B_INPUT_START,
        "payload": {
            "id": next_id,
        },
    }


def set_channel_b_success(next_id):
    return {
        "type": SET_CHANNEL_B_INPUT_SUCCESS,
        "payload": {
            "id": next_id,
        },
    }


def set_channel_b_error(requested_id, next_id):
    return {
        "type": SET_CHANNEL_B_INPUT_ERROR,
        "payload": {
            "requested_id": requested_id,
            "id": next_id,
        },
    }



def set_channel_b_cancel(channel_id):
    return {
        "type": SET_CHANNEL_B_INPUT_CANCEL,
        "payload": {
            "id": channel_id,
        },
    }




def _make_dispatch(client):

    def dispatch(action):
        payload = json.dumps(action["payload"])
        topic = config.mqttbasetopic + "/" + action["type"]

        client.publish(topic, payload)

    return dispatch


def handle(dispatch, action):
    payload = action["payload"]

    if action["type"] == GET_CHANNEL_INPUTS_REQUEST:
        dispatch(get_channel_inputs_success())

    elif action["type"] == SET_CHANNEL_A_INPUT_REQUEST:
        channel_id = payload.get("id", 0)
        hdmi.select_a(channel_id)

        next_id = hdmi.get_selected(hdmi.STATE_A_PINS)
        if next_id == channel_id:
            dispatch(set_channel_a_success(next_id))
        else:
            dispatch(set_channel_a_error(channel_id, next_id))

    elif action["type"] == SET_CHANNEL_B_INPUT_REQUEST:
        channel_id = payload.get("id", 0)
        hdmi.select_b(channel_id)

        next_id = hdmi.get_selected(hdmi.STATE_B_PINS)
        if next_id == channel_id:
            dispatch(set_channel_b_success(next_id))
        else:
            dispatch(set_channel_b_error(channel_id, next_id))


def _make_mqtt_callback(client):
    dispatch = _make_dispatch(client)

    def mqtt_callback(topic, msg):
        topic = topic.decode()
        payload = json.loads(msg.decode())

        action_type = topic.split("/")[-1]

        action = {
            "type": action_type,
            "payload": payload,
        }

        handle(dispatch, action)

    return mqtt_callback


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
        except Exception as e:
            print(e)
            pass
        time.sleep(0.25)


def main():

    # Connect to wifi
    w = wifi.Wifi(config.ssid, config.password, config.ifconfig)
    if not w.connect():
        print("Could not connect to wifi")
        machine.reset()

    time.sleep_ms(300)

    print("Connecting to MQTT")

    c = mqtt.MQTTClient('umqtt_client',
                        config.mqttserver,
                        port=config.mqttport)
    c.DEBUG = True
    c.set_callback(_make_mqtt_callback(c))

    _mqtt_connect(c)

    while True:
        c.wait_msg()


try:
    main()
except:
    raise
    machine.reset()



