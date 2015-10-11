#!/usr/local/bin/python3

import sys
import time
import signal
import subprocess


def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)


def sleep_and_speak(num, second=1):
    time.sleep(second)
    subprocess.call(['say', str(num)])


if __name__ == '__main__':
    dst = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    signal.signal(signal.SIGINT, signal_handler)
    i = 0
    while True:
        i += 1
        print('Total: {}, Current: {}.'.format(dst, i))
        sleep_and_speak(1)
        sleep_and_speak(2)
        sleep_and_speak(3)
        sleep_and_speak(4)
        sleep_and_speak(5)
        if i == dst:
            subprocess.call(['say', 'stop, relax. wait a moment'])
            break
