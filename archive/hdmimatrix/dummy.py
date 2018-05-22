#!/usr/bin/env python3

"""
Hdmi Matrix simulation
"""

import time
from datetime import datetime

from llama import mqtt

import hdmi

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

PING = "@meta/PING"
PONG = "@meta/PONG"
WHOIS = "@meta/WHOIS"
IAMA = "@meta/IAMA"

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


def pong(handle):
    return {
        "type": PONG,
        "payload": {
            "handle": handle,
            "timestamp": int(datetime.utcnow().timestamp() * 1000)
        }
    }


def iama(manifest):
    return {
        "type": IAMA,
        "payload": manifest,
    }


def handle_meta(dispatch, action, manifest):
    """
    Implement meta actions / service discovery
    """
    if action["type"] == PING:
        _handle_ping(dispatch, action)
    elif action["type"] == WHOIS:
        _handle_whois(dispatch, action, manifest)


def _handle_ping(dispatch, action):
    """Reply with PONG"""
    handle = "hdmimatrix@dummy"
    if action["payload"] == handle or action["payload"] == "*":
        dispatch(pong(handle))


def _handle_whois(dispatch, action, manifest):
    """Reply with iama"""
    handle = "hdmimatrix@dummy"
    if action["payload"] == handle or action["payload"] == "*":
        dispatch(iama(manifest))


def main(args):

    dispatch, receive = mqtt.connect("localhost:1883", {
        "hdmi": "v1/mainhall/hdmimatrix",
        "meta": "v1/_meta",
    })

    print("MQTT connected.")

    iama = {
        "handle": "hdmimatrix@dummy",
        "name": "hdmimatrix-mqtt",
        "version": "0.0.1",
        "description": "Bridge HDMI-Matrix to MQTT",
        "started_at": int(datetime.utcnow().timestamp() * 1000),
    }


    for action in receive():
        print("Handling action: {}".format(action))
        handle(dispatch, action)
        handle_meta(dispatch, action, iama)

if __name__ == "__main__":
    main(None)

