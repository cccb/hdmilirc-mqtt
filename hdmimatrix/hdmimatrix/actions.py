
from hdmimatrix import switch

# Action Types
GET_SELECTED_INPUT_REQUEST = "@hdmi/GET_SELECTED_INPUT_REQUEST"
GET_SELECTED_INPUT_SUCCESS = "@hdmi/GET_SELECTED_INPUT_SUCCESS"
GET_SELECTED_INPUT_ERROR = "@hdmi/GET_SELECTED_INPUT_ERROR"

GET_SELECTED_AUDIO_MODE_REQUEST = "@hdmi/GET_SELECTED_AUDIO_MODE_REQUEST"
GET_SELECTED_AUDIO_MODE_SUCCESS = "@hdmi/GET_SELECTED_AUDIO_MODE_SUCCESS"
GET_SELECTED_AUDIO_MODE_ERROR = "@hdmi/GET_SELECTED_AUDIO_MODE_ERROR"

GET_CONNECTION_STATES_REQUEST = "@hdmi/GET_CONNECTION_STATES_REQUEST"
GET_CONNECTION_STATES_SUCCESS = "@hdmi/GET_CONNECTION_STATES_SUCCESS"
GET_CONNECTION_STATES_ERROR = "@hdmi/GET_CONNECTION_STATES_ERROR"

GET_AUTO_SELECT_REQUEST = "@hdmi/GET_AUTO_SELECT_REQUEST"
GET_AUTO_SELECT_SUCCESS = "@hdmi/GET_AUTO_SELECT_SUCCESS"
GET_AUTO_SELECT_ERROR = "@hdmi/GET_AUTO_SELECT_ERROR"

SELECT_INPUT_REQUEST = "@hdmi/SELECT_INPUT_REQUEST"
SELECT_INPUT_SUCCESS = "@hdmi/SELECT_INPUT_SUCCESS"
SELECT_INPUT_ERROR = "@hdmi/SELECT_INPUT_ERROR"


# Action Creators
def get_connection_states_success(states):
    return {
        "type": GET_CONNECTION_STATES_SUCCESS,
        "payload": {
            "connections": states,
        }
    }


def get_selected_input_request():
    return {
        "type": GET_SELECTED_INPUT_REQUEST,
        "payload": {},
    }


def get_selected_input_success(input_id):
    return {
        "type": GET_SELECTED_INPUT_SUCCESS,
        "payload": {
            "input_id": input_id,
        },
    }


def get_selected_input_error(error):
    return {
        "type": GET_SELECTED_INPUT_ERROR,
        "payload": {
            "error": error,
        },
    }


def get_auto_select_success(enabled):
    return {
        "type": GET_AUTO_SELECT_SUCCESS,
        "payload": {
            "enabled": enabled,
        },
    }

def set_auto_select_success(enabled):
    return {
        "type": SET_AUTO_SELECT_SUCCESS,
        "payload": {
            "enabled": enabled,
        }
    }

def get_selected_audio_mode_request():
    return {
        "type": GET_SELECTED_AUDIO_MODE_REQUEST,
        "payload": {},
    }


def get_selected_audio_mode_success(mode_id):
    # Resolve mode:
    modes = {
        switch.AUDIO_MODE_AUTO: "auto",
        switch.AUDIO_MODE_STEREO: "stereo",
        switch.AUDIO_MODE_5_1: "5.1",
        switch.AUDIO_MODE_7_1: "7.1",
    }

    return {
        "type": GET_SELECTED_AUDIO_MODE_SUCCESS,
        "payload": {
            "mode_id": mode_id,
            "mode": modes[mode_id],
        },
    }


def get_selected_audio_mode_error(mode_id, error):
    return {
        "type": GET_SELECTED_AUDIO_MODE_ERROR,
        "payload": {
            "error": error,
            "mode_id": mode_id,
        },
    }


def select_input_success(input_id):
    return {
        "type": SELECT_INPUT_SUCCESS,
        "payload": {
            "input_id": input_id,
        },
    }

def select_input_error(input_id, error):
    return {
        "type": SELECT_INPUT_ERROR,
        "payload": {
            "input_id": input_id,
            "error": error,
        }
    }
