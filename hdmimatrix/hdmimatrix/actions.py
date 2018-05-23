
from hdmimatrix import switch

# Action Types

GET_SELECTED_INPUT_REQUEST = "@hdmi/GET_SELECTED_INPUT_REQUEST"
GET_SELECTED_INPUT_SUCCESS = "@hdmi/GET_SELECTED_INPUT_SUCCESS"
GET_SELECTED_INPUT_ERROR = "@hdmi/GET_SELECTED_INPUT_ERROR"

GET_AUDIO_MODE_REQUEST = "@hdmi/GET_AUDIO_MODE_REQUEST"
GET_AUDIO_MODE_SUCCESS = "@hdmi/GET_AUDIO_MODE_SUCCESS"
GET_AUDIO_MODE_ERROR = "@hdmi/GET_AUDIO_MODE_ERROR"

GET_CONNECTION_STATES_REQUEST = "@hdmi/GET_CONNECTION_STATES_REQUEST"
GET_CONNECTION_STATES_SUCCESS = "@hdmi/GET_CONNECTION_STATES_SUCCESS"
GET_CONNECTION_STATES_ERROR = "@hdmi/GET_CONNECTION_STATES_ERROR"

GET_AUTO_SELECT_REQUEST = "@hdmi/GET_AUTO_SELECT_REQUEST"
GET_AUTO_SELECT_SUCCESS = "@hdmi/GET_AUTO_SELECT_SUCCESS"
GET_AUTO_SELECT_ERROR = "@hdmi/GET_AUTO_SELECT_ERROR"


UPDATE_SELECTED_INPUT_REQUEST = "@hdmi/UPDATE_SELECTED_INPUT_REQUEST"
UPDATE_SELECTED_INPUT_SUCCESS = "@hdmi/UPDATE_SELECTED_INPUT_SUCCESS"
UPDATE_SELECTED_INPUT_ERROR = "@hdmi/UPDATE_SELECTED_INPUT_ERROR"

UPDATE_AUDIO_MODE_REQUEST = "@hdmi/UPDATE_AUDIO_MODE_REQUEST"
UPDATE_AUDIO_MODE_SUCCESS = "@hdmi/UPDATE_AUDIO_MODE_SUCCESS"
UPDATE_AUDIO_MODE_ERROR = "@hdmi/UPDATE_AUDIO_MODE_ERROR"

UPDATE_AUTO_SELECT_REQUEST = "@hdmi/UPDATE_AUTO_SELECT_REQUEST"
UPDATE_AUTO_SELECT_SUCCESS = "@hdmi/UPDATE_AUTO_SELECT_SUCCESS"
UPDATE_AUTO_SELECT_ERROR = "@hdmi/UPDATE_AUTO_SELECT_ERROR"


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


def update_selected_input_success(input_id):
    return {
        "type": UPDATE_SELECTED_INPUT_SUCCESS,
        "payload": {
            "input_id": input_id,
        }
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


def update_auto_select_success(enabled):
    return {
        "type": UPDATE_AUTO_SELECT_SUCCESS,
        "payload": {
            "enabled": enabled,
        }
    }



#
# Audio Mode

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

def update_audio_mode_success(mode_id):
    return {
        "type": UPDATE_AUDIO_MODE_SUCCESS,
        "payload": {
            "mode_id": mode_id,
            "mode": switch.resolve_audio_mode(mode_id),
        },
    }


