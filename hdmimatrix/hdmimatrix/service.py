
"""
HDMI MQTT Service
"""

# Warning: I am not proud of this code.

from hdmimatrix import switch
from hdmimatrix import actions as hdmi_actions


INITIAL_STATE = {
    "connections": [],
    "connections_error": None,

    "selected_input": -1,
    "selected_input_error": None,

    "audio_mode": -1,
    "audio_mode_error": None,

    "auto_select": None,
    "auto_select_error": None,
}


def _get_state(conn):
    """Get initial state from HDMI switch"""
    try:
        connections = switch.get_connection_state(conn)
        connections_error = None
    except switch.ChecksumError:
        connections = [False, False, False, False, False]
        connections_error = "Could not get state of connected devices"

    try:
        selected_input = switch.get_selected_input(conn)
        selected_input_error = None
    except switch.ChecksumError:
        selected_input = 0
        selected_input_error = "Could not get selected input id"

    try:
        audio_mode = switch.get_selected_audio_mode(conn)
        audio_mode_error = None
    except switch.ChecksumError:
        audio_mode = 0
        audio_mode_error = "Could not get selected audio mode"

    try:
        auto_select = switch.get_auto_switch_state(conn)
        auto_select_error = None
    except switch.ChecksumError:
        auto_select = False
        auto_select_error = "Could not get auto select state"

    state = {
        "connections": connections,
        "connections_error": connections_error,

        "selected_input": selected_input,
        "selected_input_error": selected_input_error,

        "audio_mode": audio_mode,
        "audio_mode_error": audio_mode_error,

        "auto_select": auto_select,
        "auto_select_error": auto_select_error,
    }

    return state


def _dispatch_state_diff(dispatch, state, next_state):
    """Dispatch state changes"""
    # Connections
    if state["connections"] != next_state["connections"]:
        dispatch(
            hdmi_actions.get_connection_states_success(
                next_state["connections"]))

    if state["connections_error"] != next_state["connections_error"] \
        and next_state["connections_error"]:
            dispatch(
                hdmi_actions.get_connection_states_error(
                    next_state["connections_error"]))


    # Auto Select State
    if state["auto_select"] != next_state["auto_select"]:
        dispatch(
            hdmi_actions.set_auto_select_success(
                next_state["auto_select"]))

    if state["auto_select_error"] != next_state["auto_select_error"] \
        and next_state["auto_select_error"]:
            dispatch(
                hdmi_actions.set_auto_select_error(
                    next_state["auto_select_error"]))


    # Selected Input / Source
    if state["selected_input"] != next_state["selected_input"]:
        dispatch(
            hdmi_actions.set_selected_input_success(
                next_state["selected_input"]))

    if state["selected_input_error"] != next_state["selected_input_error"] \
        and next_state["selected_input_error"]:
            dispatch(
                hdmi_actions.set_selected_input_error(
                    next_state["selected_input"],
                    next_state["selected_input_error"]))


    # Selected Audio Mode
    if state["audio_mode"] != next_state["audio_mode"]:
        dispatch(
            hdmi_actions.set_audio_mode_success(
                next_state["audio_mode"]))

    if state["audio_mode_error"] != next_state["audio_mode_error"] \
        and next_state["audio_mode_error"]:
            dispatch(
                hdmi_actions.set_audio_mode_error(
                    next_state["audio_mode"],
                    next_state["audio_mode_error"]))


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
                hdmi_actions.get_selected_input_success(
                    state["selected_input"]))

        elif action["type"] == hdmi_actions.GET_AUTO_SELECT_REQUEST:
            dispatch(
                hdmi_actions.get_auto_select_success(
                    state["auto_select"]))

        elif action["type"] == hdmi_actions.GET_AUDIO_MODE_REQUEST:
            dispatch(
                hdmi_actions.get_audio_mode_success(
                    state["audio_mode"]))

        elif action["type"] == hdmi_actions.GET_CONNECTION_STATES_REQUEST:
            dispatch(
                hdmi_actions.get_connection_states_success(
                    state["connections"]))

        # Select Input Id
        elif action["type"] == hdmi_actions.SET_SELECTED_INPUT_REQUEST:
            selected_input = int(action["payload"].get("input_id", 0))
            try:
                switch.select_source(conn, selected_input)
                state["selected_input"] = selected_input

                dispatch(
                    hdmi_actions.set_selected_input_success(
                        selected_input))


            except Exception as e:
                dispatch(
                    hdmi_actions.set_selected_input_error(
                        selected_input, str(e)))


        # Audio Mode
        elif action["type"] == hdmi_actions.SET_AUDIO_MODE_REQUEST:
            audio_mode = int(action["payload"].get("mode_id", 0))
            try:
                switch.select_audio_mode(conn, audio_mode)
                state["audio_mode"] = audio_mode

                dispatch(
                    hdmi_actions.set_audio_mode_success(audio_mode))

            except Exception as e:
                dispatch(
                    hdmi_actions.set_audio_mode_error(
                        audio_mode, str(e)))

        # Auto Select Mode
        elif action["type"] == hdmi_actions.SET_AUTO_SELECT_REQUEST:
            enabled = action["payload"].get("enabled", False)
            try:
                switch.set_auto_switch(conn, enabled)
                state["auto_select"] = enabled

                dispatch(
                    hdmi_actions.set_auto_select_success(enabled))

            except Exception as e:
                dispatch(
                    hdmi_actions.set_auto_select_error(str(e)))

