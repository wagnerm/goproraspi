'''

@author: Max Wagner

For a given interval and time period take pictures
with a go pro using the go pro app api.
'''

import sys
import os
import goprohero
import argparse
import logging
import time
import datetime


def take_picture(camera):
    logging.info(camera.status())

def process(args):
    wait_delta = datetime.timedelta(seconds=float(args.time))
    interval_delta = datetime.timedelta(seconds=float(args.interval))
    start = datetime.datetime.now()
    while True:
        # do stuff
        take_picture(gopro)
        current = datetime.datetime.now()
        if current + interval_delta >= start + wait_delta:
            break
        logging.info("Running {} for {}".format(current + interval_delta, start + wait_delta))
        time.sleep(float(args.interval))


def main(argv=None):
    program_name = os.path.basename(sys.argv[0])

    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', help='IP Address of Go Pro', required=False, default="10.5.5.9")
    parser.add_argument('-p', '--password', help='WiFi password of Go Pro', required=True, default='')
    parser.add_argument('-i', '--interval', help='Interval on which a picture will be taken (in seconds)', required=False, default=60)
    parser.add_argument('-t', '--time', help='Duration of the timelapse (in minutes)', required=False, default=60)
    args = parser.parse_args()

    log_format = '%(asctime)s   %(message)s'
    logging.basicConfig(format=log_format, level=logging.INFO)

    gopro = GoProHero([args.ip, args.password])
    process(args, gopro)

if __name__ == "__main__":
    sys.exit(main())
