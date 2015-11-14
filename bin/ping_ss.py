#!/usr/local/bin/python3
import sys
import json
import subprocess

from termcolor import colored
from os.path import expanduser


def do_ping(item):
    print('======== Current {} {} ========'.format(item['name'], item['url']))
    result = subprocess.Popen(['ping', '-c5', '-W300', item['url']],
                              stdout=subprocess.PIPE).stdout.read()
    print(colored('\n'.join(result.decode().split('\n')[-3:-1]), 'green'))
    print('======== end ========')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('参数数量不足')
        sys.exit(1)
    if len(sys.argv) > 2:
        print('参数太多')
        sys.exit(2)

    PATH = expanduser(sys.argv[1])
    data = []
    with open(PATH, 'r') as f:
        data = json.loads(f.read())
    for i in data:
        do_ping(i)
