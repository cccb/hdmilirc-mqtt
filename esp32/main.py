
import time
import json

import machine

import config
import wifi
import mqtt


# Update lock
DEADTIME = 1.0

# Update lock timer
LAST_UPDATE_A_FINISHED = 0
LAST_UPDATE_B_FINISHED = 0


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


def _in_deadtime(last_update):
    return (time.time() - last_update <= DEADTIME)


def handle(dispatch, action):
    global LAST_UPDATE_A_FINISHED
    global LAST_UPDATE_B_FINISHED

    payload = action["payload"]

    if action["type"] == GET_CHANNEL_INPUTS_REQUEST:
        dispatch(get_channel_inputs_success())

    elif action["type"] == SET_CHANNEL_A_INPUT_REQUEST:
        channel_id = payload.get("id", 0)

        # Check deadtime
        if _in_deadtime(LAST_UPDATE_A_FINISHED):
            dispatch(set_channel_a_cancel(channel_id))
            return

        # Begin update
        dispatch(set_channel_a_start(channel_id))

        # This might take a while
        hdmi.select_a(channel_id)

        # Check result
        next_id = hdmi.get_selected(hdmi.STATE_A)
        if next_id == channel_id:
            dispatch(set_channel_a_success(next_id))
        else:
            dispatch(set_channel_a_error(channel_id, next_id))

        LAST_UPDATE_A_FINISHED = time.time()


    elif action["type"] == SET_CHANNEL_B_INPUT_REQUEST:
        channel_id = payload.get("id", 0)

        # Check deadtime
        if _in_deadtime(LAST_UPDATE_B_FINISHED):
            dispatch(set_channel_b_cancel(channel_id))
            return

        # Begin
        dispatch(set_channel_b_start(channel_id))
        hdmi.select_b(channel_id)

        next_id = hdmi.get_selected(hdmi.STATE_B)
        if next_id == channel_id:
            dispatch(set_channel_b_success(next_id))
        else:
            dispatch(set_channel_b_error(channel_id, next_id))

        LAST_UPDATE_B_FINISHED = time.time()



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



