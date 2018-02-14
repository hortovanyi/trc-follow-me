import time
import asyncio
import argparse
import serial
import csv
import io
from threading import Thread
import pandas as pd
import numpy as np
import cv2
from datetime import datetime

import actuators

lastActuators = actuators.Actuators()

port = serial.Serial(
    port="/dev/cu.TIVCP3410440",
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=3.0,
    rtscts=False)

async def actuator_read():
    global lastActuators

    print ("waiting for next serial read")
    data = port.readline()

    lastActuators.update(data)

    print (lastActuators)


def actuator_background_update():

    while True:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(actuator_read())


def start_loop(loop):

    # asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        # Canceling pending tasks and stopping the loop
        asyncio.gather(*asyncio.Task.all_tasks()).cancel()

        # Stopping the loop
        loop.stop()

        # Received Ctrl+C
        loop.close()


def main():
    print('server starting ...')

    print("starting actuator update thread")
    # actuator_loop = asyncio.new_event_loop()
    # actuator_thread = Thread(target=start_loop, args=(actuator_loop,))

    # print("Initiating actuator background update")
    # actuator_loop.call_soon_threadsafe(actuator_background_update)

    actuator_thread = Thread(target=actuator_background_update)
    actuator_thread.start()

    print('running')

    print('setup camera collection ... ')
    start_time = datetime.now()

    image_csv_log_filename = '%d_images_log.csv' % start_time.timestamp()

    cap = cv2.VideoCapture(0)
    dir_path = 'images'
    global lastActuators


    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            mytime = datetime.now()
            steering = lastActuators.steering

            # create full image name
            image_name = mytime.strftime("%Y_%b_%d_%H_%M_%S_%f")+'.png'
            full_name = '%s/%s' % (dir_path, image_name)

            print ('writing ', full_name)
            cv2.imwrite(full_name, frame)

            with open(image_csv_log_filename, 'a') as f:
                data = '%f,%s,%f\n' % (mytime.timestamp(), full_name, steering)
                #print(data)
                f.write(data)


    except KeyboardInterrupt:
        print ('KeyboardInterrupt')
        # Canceling pending tasks and stopping the loop
        asyncio.gather(*asyncio.Task.all_tasks()).cancel()


if __name__ == '__main__':
    main()
