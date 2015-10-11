#!/usr/local/bin/python3

import sys


def get_file_encoding_content(filename, coding='gbk'):
    content = ''
    with open(filename, 'rb') as f:
        content = f.read().decode(coding)
    return content


def show_file_content(filename, coding='gbk'):
    content = get_file_encoding_content(filename, coding)
    print(content)


def encode_to_new_file(filename, new_filename, coding='gbk'):
    content = get_file_encoding_content(filename, coding)

    with open(new_filename, 'w') as f:
        f.write(content)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        show_file_content(sys.argv[1])
    elif len(sys.argv) == 3:
        encode_to_new_file(sys.argv[1], sys.argv[2])
    else:
        print('参数数量错误')
