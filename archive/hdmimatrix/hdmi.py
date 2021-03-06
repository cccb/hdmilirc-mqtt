
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
    global STATE_A
    STATE_A = next_channel(STATE_A)

    return get_selected(STATE_A)


def next_b():
    global STATE_B
    STATE_B = next_channel(STATE_B)

    return get_selected(STATE_B)


def next_channel(state):
    selected = get_selected(state)
    if selected == -1:
        return -1

    time.sleep(0.65) # almost a second per click

    state = [state[-1]]+state[:-1]

    return state


def select_a(chan):
    if chan > 3 or chan < 0 or \
       chan == get_selected(STATE_A):
        return -1

    while True:
        next_chan = next_a()
        print("A is now: {}".format(next_chan))
        if next_chan == chan:
            return

        time.sleep(0.25)



def select_b(chan):
    if chan > 3 or chan < 0 or \
       chan == get_selected(STATE_B):
        return -1

    while True:
        next_chan = next_b()
        print("B is now: {}".format(next_chan))
        if next_chan == chan:
            return

        time.sleep(0.25)


