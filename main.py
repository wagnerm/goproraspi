#!/usr/bin/env python

'''

@author: Max Wagner

For a given interval and time period take pictures
with a go pro using the go pro app api.
'''

import sys
import os
from goprohero import GoProHero
import argparse
import logging
import time
import datetime
import dateutil.parser


def wait(begin_time):
   begin = dateutil.parser.parse(begin_time)
   while True:
       now = datetime.datetime.now()
       logging.info("Begin at: {}, now: {}".format(begin, now))
       if now >= begin:
           return
       time.sleep(10)


def wait_for_camera(camera, maxwait=600):
    '''
    Wait for camera to respond
    If the camera is in 'sleeping' state, power on
    If camera is in 'on' state, return
    '''
    interval = 5
    wait_delta = datetime.timedelta(seconds=maxwait)
    interval_delta = datetime.timedelta(seconds=5)
    start = datetime.datetime.now()
    while True:
        status = camera.status()
        if status.get('summary') in 'notfound':
            logging.info("Camera not found")
        elif status.get('summary') in 'on':
            return
        elif status.get('summary') in 'sleeping':
            camera.command('power', 'on')
        current = datetime.datetime.now()
        if current + interval_delta >= start + wait_delta:
            break
        cur_secs = maxwait - ((start + wait_delta) - (current + interval_delta)).seconds
        logging.info("Waiting on camera for {} of {} seconds".format(cur_secs, maxwait))
        time.sleep(interval)
    raise Exception("Cannot get to camera")


def take_picture(camera):
    '''Put camera in still mode if needed, record on to take picture'''
    status = camera.status()
    if status.get('mode') and status.get('mode') not in 'still':
        camera.command('mode', 'still')
    camera.command('record', 'on')


def process(args, camera):
    if args.begin:
        logging.info("Will wait until {} to start.".format(args.begin))
        wait(args.begin)
    wait_for_camera(camera)
    wait_delta = datetime.timedelta(minutes=args.time)
    interval_delta = datetime.timedelta(seconds=args.interval)
    start = datetime.datetime.now()
    while True:
        take_picture(camera)
        current = datetime.datetime.now()
        if current + interval_delta >= start + wait_delta:
            break
        cur_secs = args.time * 60 - ((start + wait_delta) - (current + interval_delta)).seconds
        logging.info("Running for {} of {} seconds".format(cur_secs, args.time * 60))
        time.sleep(float(args.interval))

    # Wait a few seconds for the camera to finish current operation to power sleep
    time.sleep(10)
    camera.command('power', 'sleep')

    logging.info('Done.')


def main(argv=None):
    program_name = os.path.basename(sys.argv[0])

    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', help='IP Address of Go Pro', required=False, default="10.5.5.9")
    parser.add_argument('-p', '--password', help='WiFi password of Go Pro', required=True, default='')
    parser.add_argument('-i', '--interval', help='Interval on which a picture will be taken (in seconds)', required=False, type=int, default=60)
    parser.add_argument('-t', '--time', help='Duration of the timelapse (in minutes)', required=False, type=int, default=60)
    parser.add_argument('-b', '--begin', help='Begin time of timelapse, UTC, ISO8601 format', required=False, default=None)
    args = parser.parse_args()

    log_format = '%(asctime)s   %(message)s'
    logging.basicConfig(format=log_format, level=logging.INFO)

    camera = GoProHero(args.ip, args.password)
    process(args, camera)

if __name__ == "__main__":
    sys.exit(main())
