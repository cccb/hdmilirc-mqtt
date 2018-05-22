
import argparse
import logging

from llama import mqtt

from hdmimatrix import switch
from hdmimatrix import service

def parse_args():
    """Parse commandline arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--broker",
                        required=True,
                        help="The MQTT broker host and port")
    parser.add_argument("-t", "--topic",
                        default="hdmimatrix",
                        help="The MQTT topic to subscribe")
    parser.add_argument("-s", "--serial",
                        required=True,
                        help="The serial device")

    return parser.parse_args()


def main(args):
    print("HDMI to MQTT\t\t\t\t\t\t\tv.0.23.42")
    print()

    # Open serial connection
    conn = switch.connect(args.serial)

    # Open MQTT connection 
    dispatch, receive = mqtt.connect(args.broker, {
        "hdmi": args.topic,
    })

    logging.info("Connected to serial and broker. Awaiting actions.")

    # Main loop: Poll HDMI matrix, check for state updates,
    # Dispatch events on change.
    service.handle(conn, dispatch, receive(timeout=1.0))
    
