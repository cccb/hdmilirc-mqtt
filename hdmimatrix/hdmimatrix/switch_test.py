
from hdmimatrix import switch


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


