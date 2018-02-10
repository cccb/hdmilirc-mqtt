
import machine
import time

STATE_A_PINS = [
    machine.Pin(16, machine.Pin.IN),
    machine.Pin(4, machine.Pin.IN),
    machine.Pin(2, machine.Pin.IN),
    machine.Pin(15, machine.Pin.IN),
]

STATE_B_PINS = [
    machine.Pin(34, machine.Pin.IN),
    machine.Pin(35, machine.Pin.IN),
    machine.Pin(5, machine.Pin.IN),
    machine.Pin(25, machine.Pin.IN),
]

BT_A = machine.Pin(13, machine.Pin.OUT, machine.Pin.PULL_DOWN)
BT_B = machine.Pin(12, machine.Pin.OUT, machine.Pin.PULL_DOWN)
BT_RST = machine.Pin(14, machine.Pin.OUT, machine.Pin.PULL_DOWN)

BT_A.value(0)
BT_B.value(0)
BT_RST.value(0)


def get_state(pins):
    """Get state from pins"""
    return [p.value() for p in pins]


def get_selected(pins):
    """Check which pin is high"""
    state = get_state(pins)
    for i, s in enumerate(state):
        if s == 1:
            return i

    return -1


def next_a():
    next_channel(BT_A, STATE_A_PINS)


def next_b():
    next_channel(BT_B, STATE_B_PINS)


def next_channel(bt, state):
    selected = get_selected(state)
    if selected == -1:
        return -1

    while True:
        # Push button
        bt.value(1)
        next_selected = get_selected(state)
        time.sleep(0.1)

        if next_selected != selected:
            bt.value(0)
            return next_selected


def select(bt, state, chan):
    if chan > 3 or chan < 0:
        return

    if chan == get_selected(state):
        return

    while True:
        next_chan = next_channel(bt, state)
        if next_chan == chan:
            return

        time.sleep(0.25)


def select_a(chan):
    select(BT_A, STATE_A_PINS, chan)


def select_b(chan):
    select(BT_B, STATE_B_PINS, chan)
