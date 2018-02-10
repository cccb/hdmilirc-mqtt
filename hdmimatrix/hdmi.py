
import time

"""
Dummy hdmi module
"""

STATE_A = [0, 1, 0, 0]
STATE_B = [1, 0, 0, 0]


def get_state(pins):
    """Get state from pins"""
    return pins


def get_selected(pins):
    state = get_state(pins)
    for i, s in enumerate(state):
        if s == 1:
            return i

    return -1

def next_a():
    return next_channel(STATE_A_PINS)


def next_b():
    return next_channel(STATE_B_PINS)


def next_channel(state):
    selected = get_selected(state)
    if selected == -1:
        return -1

    time.sleep(0.8) # almost a second per click

    state = [state[-1]]+[state[:-1]]
    return state


def select(state, chan):
    if chan > 3 or chan < 0:
        return

    if chan == get_selected(state):
        return

    while True:
        next_chan = next_channel(state)
        if next_chan == chan:
            return

        time.sleep(0.25)


def select_a(chan):
    select(STATE_A, chan)


def select_b(chan):
    select(STATE_B, chan)

