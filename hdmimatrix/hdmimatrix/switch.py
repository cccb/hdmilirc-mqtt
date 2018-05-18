"""
Implements the serial communication protocoll,
which is used by the Ligawo HDR Switch 4x1
"""


import serial
import time


# What we found so far:
#
# A packet is always 13 byes long.
#
# bytes[0:2] Something like begin packet,
# bytes[12]  Most likely a checksum
#
#  CHECK = bytes[0] + bytes[1] - SUM_2^11(bytes)
#
# seems to be it.
#

GET_SELECTED_INPUT = b'\xA5\x5B\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\xFC'
GET_SELECTED_AUDIO = b'\xA5\x5B\x01\x0C\x01\x00\x00\x00\x00\x00\x00\x00\xF2'

SELECT_INPUT_0 = b'\xA5\x5B\x02\x03\x01\x00\x01\x00\x00\x00\x00\x00\xF9'
SELECT_INPUT_1 = b'\xA5\x5B\x02\x03\x02\x00\x01\x00\x00\x00\x00\x00\xF8'
SELECT_INPUT_2 = b'\xA5\x5B\x02\x03\x03\x00\x01\x00\x00\x00\x00\x00\xF7'
SELECT_INPUT_3 = b'\xA5\x5B\x02\x03\x04\x00\x01\x00\x00\x00\x00\x00\xF6'

SELECT_AUDIO_MODE_0 = b'\xA5\x5B\x03\x02\x01\x00\x01\x00\x00\x00\x00\x00\xF9'
SELECT_AUDIO_MODE_1 = b'\xA5\x5B\x03\x02\x02\x00\x01\x00\x00\x00\x00\x00\xF8'
SELECT_AUDIO_MODE_2 = b'\xA5\x5B\x03\x02\x03\x00\x01\x00\x00\x00\x00\x00\xF7'
SELECT_AUDIO_MODE_3 = b'\xA5\x5B\x03\x02\x04\x00\x01\x00\x00\x00\x00\x00\xF6'

GET_INPUT_STATE_0 = b'\xA5\x5B\x01\x04\x01\x00\x00\x00\x00\x00\x00\x00\xFA'
GET_INPUT_STATE_1 = b'\xA5\x5B\x01\x04\x02\x00\x00\x00\x00\x00\x00\x00\xF9'
GET_INPUT_STATE_2 = b'\xA5\x5B\x01\x04\x03\x00\x00\x00\x00\x00\x00\x00\xF8'
GET_INPUT_STATE_3 = b'\xA5\x5B\x01\x04\x04\x00\x00\x00\x00\x00\x00\x00\xF7'

GET_OUTPUT_STATE = b'\xA5\x5B\x01\x05\x01\x00\x00\x00\x00\x00\x00\x00\xF9'

GET_AUTO_SWITCH_STATE = b'\xA5\x5B\x01\x0D\x00\x00\x00\x00\x00\x00\x00\x00\xF2'

SET_AUTO_SWITCH_ON = b'\xA5\x5B\x02\x05\x0F\x00\x00\x00\x00\x00\x00\x00\xEA'
SET_AUTO_SWITCH_OFF = b'\xA5\x5B\x02\x05\xF0\x00\x00\x00\x00\x00\x00\x00\x09'


def _request(conn, payload):
    """
    Query HDMI switch via serial interface.

    :param conn: A serial connection
    :type conn: serial.Serial

    :param payload: The payload bytes to transmit
    :type payload: bytes
    """
    conn.write(payload[:1])
    time.sleep(0.001)
    conn.write(payload[1:])

    return conn.read(response_len)


def _checksum(packet):
    """
    Calculate the packet's checksum

    :param packet: The packet to check
    :type packet: bytes

    :rtype: int
    """
    return packet[0] + packet[1] - sum(packet[2:12])


def _validate_packet(packet):
    """
    Check if the packet's checksum is valid

    :param packet: The packet to check
    :type packet: bytes

    :rtype: bool
    """
    if len(packet) != 13:
        return False

    return _checksum(packet) == packet[-1]


def _decode_index(packet):
    """Decode integer index value of response packet."""
    return packet[6] - 1


def get_selected_source(conn):
    """Retrieve the selected source id. Zero indexed."""
    response = request(conn, GET_INPUT_PAYLOAD)
    if not _validate_packet(response):
        return -1

    return _decode_index(response)


def get_selected_audio_mode(conn):
    """Get the selected audio mode"""
    response = request(conn, GET_AUDIO_PAYLOAD);
    if not _validate_packet(response):
        return -1

    return _decode_index(response)


