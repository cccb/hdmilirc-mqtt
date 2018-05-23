
from hdmimatrix import switch

# Action Types

GET_SELECTED_INPUT_REQUEST = "@hdmi/GET_SELECTED_INPUT_REQUEST"
GET_SELECTED_INPUT_SUCCESS = "@hdmi/GET_SELECTED_INPUT_SUCCESS"
GET_SELECTED_INPUT_ERROR = "@hdmi/GET_SELECTED_INPUT_ERROR"

SET_SELECTED_INPUT_REQUEST = "@hdmi/SET_SELECTED_INPUT_REQUEST"
SET_SELECTED_INPUT_SUCCESS = "@hdmi/SET_SELECTED_INPUT_SUCCESS"
SET_SELECTED_INPUT_ERROR = "@hdmi/SET_SELECTED_INPUT_ERROR"

GET_AUDIO_MODE_REQUEST = "@hdmi/GET_AUDIO_MODE_REQUEST"
GET_AUDIO_MODE_SUCCESS = "@hdmi/GET_AUDIO_MODE_SUCCESS"
GET_AUDIO_MODE_ERROR = "@hdmi/GET_AUDIO_MODE_ERROR"

SET_AUDIO_MODE_REQUEST = "@hdmi/SET_AUDIO_MODE_REQUEST"
SET_AUDIO_MODE_SUCCESS = "@hdmi/SET_AUDIO_MODE_SUCCESS"
SET_AUDIO_MODE_ERROR = "@hdmi/SET_AUDIO_MODE_ERROR"

GET_AUTO_SELECT_REQUEST = "@hdmi/GET_AUTO_SELECT_REQUEST"
GET_AUTO_SELECT_SUCCESS = "@hdmi/GET_AUTO_SELECT_SUCCESS"
GET_AUTO_SELECT_ERROR = "@hdmi/GET_AUTO_SELECT_ERROR"

SET_AUTO_SELECT_REQUEST = "@hdmi/SET_AUTO_SELECT_REQUEST"
SET_AUTO_SELECT_SUCCESS = "@hdmi/SET_AUTO_SELECT_SUCCESS"
SET_AUTO_SELECT_ERROR = "@hdmi/SET_AUTO_SELECT_ERROR"

GET_CONNECTION_STATES_REQUEST = "@hdmi/GET_CONNECTION_STATES_REQUEST"
GET_CONNECTION_STATES_SUCCESS = "@hdmi/GET_CONNECTION_STATES_SUCCESS"
GET_CONNECTION_STATES_ERROR = "@hdmi/GET_CONNECTION_STATES_ERROR"

# Action Creators

#
# Selected Input
#
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


def set_selected_input_request(input_id):
    return {
        "type": SET_SELECTED_INPUT_REQUEST,
        "payload": {
            "input_id": input_id,
        },
    }


def set_selected_input_success(input_id):
    return {
        "type": SET_SELECTED_INPUT_SUCCESS,
        "payload": {
            "input_id": input_id,
        }
    }


def set_selected_input_error(input_id, error):
    return {
        "type": SET_SELECTED_INPUT_ERROR,
        "payload": {
            "input_id": input_id,
            "error": error,
        }
    }

#
# Audio Mode
#
def get_audio_mode_request():
    return {
        "type": GET_AUDIO_MODE_REQUEST,
        "payload": {},
    }


def get_audio_mode_success(mode_id):
    return {
        "type": GET_AUDIO_MODE_SUCCESS,
        "payload": {
            "mode_id": mode_id,
            "mode": switch.resolve_audio_mode(mode_id),
        },
    }


def get_audio_mode_error(error):
    return {
        "type": GET_AUDIO_MODE_ERROR,
        "payload": {
            "error": error,
        },
    }


def set_audio_mode_request(mode_id):
    return {
        "type": SET_AUDIO_MODE_REQUEST,
        "payload": {
            "mode_id": mode_id,
        },
    }


def set_audio_mode_success(mode_id):
    return {
        "type": SET_AUDIO_MODE_SUCCESS,
        "payload": {
            "mode_id": mode_id,
            "mode": switch.resolve_audio_mode(mode_id),
        },
    }

def set_audio_mode_error(mode_id, error):
    return {
        "type": SET_AUDIO_MODE_ERROR,
        "payload": {
            "mode_id": mode_id,
            "error": error,
        },
    }

#
# Auto Select
#
def get_auto_select_success(enabled):
    return {
        "type": GET_AUTO_SELECT_SUCCESS,
        "payload": {
            "enabled": enabled,
        },
    }


def get_auto_select_error(error):
    return {
        "type": GET_AUTO_SELECT_ERROR,
        "payload": {
            "error": error,
        },
    }


def set_auto_select_request(enabled):
    return {
        "type": SET_AUTO_SELECT_REQUEST,
        "payload": {
            "enabled": enabled,
        }
    }


def set_auto_select_success(enabled):
    return {
        "type": SET_AUTO_SELECT_SUCCESS,
        "payload": {
            "enabled": enabled,
        },
    }

def set_auto_select_error(error):
    return {
        "type": SET_AUTO_SELECT_ERROR,
        "payload": {
            "error": error,
        },
    }

#
# Connection States
#
def get_connection_states_request():
    return {
        "type": GET_CONNECTION_STATES_REQUEST,
        "payload": {
        },
    }

def get_connection_states_success(states):
    return {
        "type": GET_CONNECTION_STATES_SUCCESS,
        "payload": {
            "connections": states,
        },
    }

def get_connection_states_error(error):
    return {
        "type": GET_CONNECTION_STATES_ERROR,
        "payload": {
            "error": error,
        },
    }

