#!/usr/bin/env python3

"""
Hdmi Matrix simulation
"""

from llama import mqtt

# Actions
GET_CHANNEL_INPUTS_REQUEST = "@hdmi/GET_CHANNEL_INPUTS_REQUEST"
GET_CHANNEL_INPUTS_SUCCESS = "@hdmi/GET_CHANNEL_INPUTS_SUCCESS"

SET_CHANNEL_A_INPUT_REQUEST = "@hdmi/SET_CHANNEL_A_INPUT_REQUEST"
SET_CHANNEL_A_INPUT_SUCCESS = "@hdmi/SET_CHANNEL_A_INPUT_SUCCESS"
SET_CHANNEL_A_INPUT_ERROR = "@hdmi/SET_CHANNEL_A_INPUT_ERROR"

SET_CHANNEL_B_INPUT_REQUEST = "@hdmi/SET_CHANNEL_B_INPUT_REQUEST"
SET_CHANNEL_B_INPUT_SUCCESS = "@hdmi/SET_CHANNEL_B_INPUT_SUCCESS"
SET_CHANNEL_B_INPUT_ERROR = "@hdmi/SET_CHANNEL_B_INPUT_ERROR"

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


def set_channel_a_success(next_id):
    return {
        "type": SET_CHANNEL_A_INPUT_SUCCESS,
        "payload": {
            "id": next_id,
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


def handle(dispatch, action):
    payload = action["payload"]

    if action["type"] == GET_CHANNEL_INPUTS_REQUEST:
        dispatch(client, get_channel_inputs_success())
    elif action["type"] == SET_CHANNEL_A_INPUT_REQUEST:
        channel_id = payload.get("id", 0)
        hdmi.select_a(channel_id)

        next_id = hdmi.get_selected(hdmi.STATE_A)
        if next_id == channel_id:
            dispatch(set_channel_a_success(next_id))
        else:
            dispatch(set_channel_a_error(channel_id, next_id))

    elif action["type"] == SET_CHANNEL_B_INPUT_REQUEST:
        channel_id = payload.get("id", 0)
        hdmi.select_a(channel_id)

        next_id = hdmi.get_selected(hdmi.STATE_B)
        if next_id == channel_id:
            dispatch(set_channel_b_success(next_id))
        else:
            dispatch(set_channel_b_error(channel_id, next_id))


def main(args):

    dispatch, receive = mqtt.connect("localhost:1883", {
        "hdmi": "v1/mainhall/hdmimatrix",
    })

    print("MQTT connected.")

    for action in receive():
        handle(dispatch, action)


if __name__ == "__main__":
    main(None)

