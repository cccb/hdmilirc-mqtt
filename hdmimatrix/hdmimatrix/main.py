
import argparse


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



if __name__ == "__main__":
    args = parse_args()
    main(args)

