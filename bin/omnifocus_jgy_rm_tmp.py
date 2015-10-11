#!/usr/local/bin/python3
import os

from pync import Notifier
from os.path import expanduser

PATH = expanduser('~/Nutstore/omnifocus')
PREFIX = 'OmniFocus-Reminders.ics-'


def main():
    files = list(filter(lambda i: i.startswith(PREFIX), os.listdir(PATH)))
    if len(files):
        os.remove(os.path.join(PATH, PREFIX[:-1]))
        files.sort(key=lambda x: os.path.getmtime(os.path.join(PATH, x)))
        for i in files[:-1]:
            os.remove(os.path.join(PATH, i))
        src = os.path.join(PATH, files[-1])
        dst = os.path.join(PATH, PREFIX[:-1])
        os.rename(src, dst)
        Notifier.notify('清理完成', title='Omnifocus Cai')

if __name__ == '__main__':
    main()
