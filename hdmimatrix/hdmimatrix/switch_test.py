
from hdmimatrix import switch

# Some Test Responses:
INPUT_1_SELECTED = b'\xA5\x5B\x02\x01\x01\x00\x02\x00\x00\x00\x00\x00\xfa'
INPUT_2_SELECTED = b'\xA5\x5B\x02\x01\x01\x00\x03\x00\x00\x00\x00\x00\xf9'

AUTO_OFF = b'\xa5\x5b\x01\r\xf0\x00\x00\x00\x00\x00\x00\x00\x02'
AUTO_ON = b'\xa5\x5b\x01\r\x0f\x00\x00\x00\x00\x00\x00\x00\xe3'

INPUT_0_DISCONNECTED = b'\xa5\x5b\x01\x04\x01\x00\xff\x00\x00\x00\x00\x00\xfb'
INPUT_0_CONNECTED    = b'\xa5\x5b\x01\x04\x01\x00\x00\x00\x00\x00\x00\x00\xfa'

INPUT_1_DISCONNECTED = b'\xa5\x5b\x01\x04\x02\x00\xff\x00\x00\x00\x00\x00\xfa'
INPUT_1_CONNECTED = b'\xa5\x5b\x01\x04\x02\x00\x00\x00\x00\x00\x00\x00\xf9'


def test_calculate_checksum():
    # We use some known good test data
    data = b'\xA5\x5B\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\xFC'

    assert switch._checksum(data) == 0xfc


def test_validate_packet():
    # We use some known good test data
    packet = b'\xA5\x5B\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\xFC'
    assert switch._validate_packet(packet) == True

    # Corrupt data
    packet = b'\xA5\x5B\x02\x23\x01\x00\x00\x00\x00\x00\x00\x00\xFC'
    assert switch._validate_packet(packet) == False

    # Too short
    packet = b'\xA5\x5B\x00\x00\x00\x00\x00\x00\xFC'
    assert switch._validate_packet(packet) == False


def test_decode_index():
    assert switch._decode_index(INPUT_1_SELECTED) == 1
    assert switch._decode_index(INPUT_2_SELECTED) == 2


def test_decode_bool():
    assert switch._decode_bool(INPUT_1_CONNECTED) == True
    assert switch._decode_bool(INPUT_1_DISCONNECTED) == False



