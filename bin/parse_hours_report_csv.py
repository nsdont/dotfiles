#!/usr/local/bin/python3

import csv
import sys


def parse(reader):
    week = []
    statistics = []
    for i in reader:
        if len(i) and i[0] == '客户':
            i[0] = '事项'
        elif len(i) and i[0] == 'Client':
            i[0] = 'Things'
        if len(i) > 2:
            week.append(i)
        elif len(i) == 2:
            statistics.append(i)

    print('### Hours')

    print()
    print('##### Week')
    list_to_md_table(week)

    print('##### Statistics')
    list_to_md_table(statistics)


def list_to_md_table(table):
    gaps = []
    gap = ':-:'
    for i in range(len(table[0])):
        gaps.append(gap)
    table.insert(1, gaps)
    for i in table:
        print('|{}|'.format('|'.join(i)))
    print()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('参数数量太少了')
    else:
        try:
            with open(sys.argv[1]) as f:
                reader = csv.reader(f)
                parse(reader)
        except OSError:
            print('找不到该文件')
