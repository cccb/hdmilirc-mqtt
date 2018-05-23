
from hdmimatrix import switch

OP_GET_SELECTED_INPUT = b'\x02\x01'
OP_SELECT_INPUT = b'\x02\x03'

OP_GET_AUDIO_MODE = b'\x01\x0c'
OP_SELECT_AUDIO_MODE = b'\x03\x02'

OP_GET_INPUT_STATE = b'\x01\x04'
OP_GET_OUTPUT_STATE = b'\x01\x05'

OP_GET_AUTO_SWITCH_STATE = b'\x01\x0d'
OP_SET_AUTO_SWITCH_STATE = b'\x02\x05'

# Packet
P_HEADER = b'\xa5\x5b'
P_MARK = b'\x00'

class Connection:
    """
    This is a mock connection, simulating the
    HDMI swich connected via serial
    """
    def __init__(self):
        """Initialize connection stub"""
        self.tx_buffer = bytes()
        self.rx_buffer = bytes()

        self.state = {
            "selected_input": 2,
            "auto_select": False,
            "connections": [True, False, True, True, True],
            "audio_mode": switch.AUDIO_MODE_STEREO,
        }

    def read(self, count=1):
        return self.tx_buffer[:count]

    def write(self, data):
        self.rx_buffer += data

        if len(self.rx_buffer) >= 13:
            response = self.handle_packet(self.rx_buffer)

            # Fill tx buffer, clear rx buffer
            self.tx_buffer = self.encode_packet(response)
            self.rx_buffer = bytes()

    def encode_packet(self, data):
        # Pad response and add checksum
        packet = P_HEADER + data + P_MARK * (10 - len(data))
        packet = packet + bytes([switch._checksum(packet)])

        return packet

    def handle_packet(self, packet):
        op, payload = self.decode(packet)

        if op == OP_GET_SELECTED_INPUT:
            return op + P_MARK * 2 + \
                self.encode_index(self.state["selected_input"])

        elif op == OP_GET_INPUT_STATE:
            input_id = self.decode_index(payload)

            return op + P_MARK * 2 + \
                self.encode_bool(self.state["connections"][input_id])

        elif op == OP_SELECT_INPUT:
            input_id = self.decode_index(payload)
            self.state["selected_input"] = input_id

            return op + P_MARK * 2 + \
                self.encode_index(input_id)

        elif op == OP_GET_OUTPUT_STATE:
            return op + P_MARK * 2+ \
                self.encode_bool(self.state["connections"][4])

        elif op == OP_SET_AUTO_SWITCH_STATE:
            enabled = self.decode_toggle(payload)
            self.state["auto_select"] = enabled

            return op + P_MARK * 2+ \
                self.encode_bool(self.state["auto_select"])

        elif op == OP_GET_AUTO_SWITCH_STATE:
            return op + P_MARK * 2 + \
                self.encode_bool(self.state["auto_select"])

        elif op == OP_GET_AUDIO_MODE:
            return op + P_MARK * 2 + \
                self.encode_index(self.state["audio_mode"])

        elif op == OP_SELECT_AUDIO_MODE:
            audio_mode = self.decode_index(payload)
            self.state["audio_mode"] = audio_mode

            return op + P_MARK * 2 + \
                self.encode_index(audio_mode)

        else:
            print("WARNING: Invalid / unhandled op: {}, payload: {}".format(
                op, payload))

        return b'\x00' * 13

    def decode(self, packet):
        # First two bytes are a magic number
        # Next two bytes is the desired operation
        op = packet[2:4]

        # Payload is located at offset 4
        payload = packet[4]

        return (op, payload)

    def decode_index(self, value):
        return value - 1

    def encode_index(self, value):
        return bytes([value + 1])

    def decode_toggle(self, value):
        return value == 0x0f

    def encode_bool(self, value):
        if value:
            return b'\x00'

        return b'\xff'

def connect():
    return Connection()


