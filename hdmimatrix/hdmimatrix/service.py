
"""
HDMI MQTT Service
"""

from hdmimatrix import switch
from hdmimatrix import actions as hdmi_actions

INITIAL_STATE = {
    "connections": [],
    "selected_source": -1,
    "selected_audio_mode": -1,
    "auto_select": None,
}

def _get_state(conn):
    """Get initial state from HDMI switch"""
    state = {
        "connections": switch.get_source_connection_state(conn),
        "selected_source": switch.get_selected_source(conn),
        "selected_audio_mode": switch.get_selected_audio_mode(conn),
        "auto_select": switch.get_auto_switch_state(conn),
    }

    return state

def _dispatch_state_diff(dispatch, state, next_state):
    """Dispatch state changes"""
    if state["connections"] != next_state["connections"]:
        dispatch(
            hdmi_actions.get_connection_states_success(
                next_state["connections"]))

    if state["auto_select"] != next_state["auto_select"]:
        dispatch(
            hdmi_actions.get_auto_select_success(
                next_state["auto_select"]))

    if state["selected_source"] != next_state["selected_source"]:
        dispatch(
            hdmi_actions.select_input_success(
                next_state["selected_source"]))

    if state["selected_audio_mode"] != next_state["selected_audio_mode"]:
        dispatch(
            hdmi_actions.get_selected_audio_mode_success(
                next_state["selected_audio_mode"]))


def handle(conn, dispatch, actions):
    """Process incoming actions"""
    state = INITIAL_STATE

    for action in actions:
        # While no action is processes, check if something changed
        # on the hdmi switch:
        if not action:
            next_state = _get_state(conn)
            _dispatch_state_diff(dispatch, state, next_state)
            state = next_state

            continue

        # React to incoming action:
        # Querying:
        if action["type"] == hdmi_actions.GET_SELECTED_INPUT_REQUEST:
            dispatch(
                hdmi_actions.select_input_success(
                    state["selected_source"]))

        elif action["type"] == hdmi_actions.GET_AUTO_SELECT_REQUEST:
            dispatch(
                hdmi_action.get_auto_select_success(
                    state["auto_select"]))

        elif action["type"] == hdmi_actions.GET_SELECTED_AUDIO_MODE_REQUEST:
            dispatch(
                hdmi_actions.get_selected_audio_mode_success(
                    state["selected_audio_mode"]))

        elif action["type"] == hdmi_actions.GET_CONNECTION_STATES_REQUEST:
            dispatch(
                hdmi_actions.get_connection_states_success(
                    state["connections"]))

        # Changing
        elif action["type"] == hdmi_actions.SELECT_INPUT_REQUEST:
            selected_source = int(action["payload"].get("input_id", 0))
            try:
                switch.select_source(conn, selected_source)
                dispatch(hdmi_actions.select_input_success(selected_source))

                state["selected_source"] = selected_source
            except:
                dispatch(
                    hdmi_actions.select_input_error(
                        selected_source, "Could not set selected input"))



