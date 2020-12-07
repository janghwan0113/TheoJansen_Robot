from control import motor
from sys import argv
from Time import Time
import numpy as np
from time import sleep
import json
from http.client import HTTPConnection
import control
PORT = 8000


print(argv)

HALF = .3
MOTOR_SPEEDS = {
    "q": (HALF, 1), "w": (1, 1), "e": (1, HALF),
    "a": (-1, 1), "s": (0, 0), "d": (1, -1),
    "z": (-HALF, -1), "x": (-1, -1), "c": (-1, -HALF),
}


def main():
    while True:
        conn = HTTPConnection(
            f"{argv[1] if len(argv) > 1 else  'DESKTOP-10PNIUR.local'}:{PORT}")

        try:
            print(1)
            conn.request("GET", "/")
        except ConnectionRefusedError as error:
            print(error)
            sleep(1)
            continue

        print('Connected')
        res = conn.getresponse()
        while True:
            chunk = res.readline()
            if (chunk == b'\n'):
                continue
            if (not chunk):
                break

            chunk = chunk[:-1].decode()
            data = json.loads(chunk)
            print(Time(), data)
            action = data['action']
            print('action', action)
            try:
                motor(*MOTOR_SPEEDS[action])
            except KeyError as error:
                print(error)


main()
