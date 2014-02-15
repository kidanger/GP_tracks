#!/usr/bin/env python2
# coding: utf-8

import os
import sys
import re
from PIL import Image

ELEMENTS = (
    ('#', (255, 255, 255)),
    ('.', (0, 0, 0)),
    ('~', (255, 255, 0)),
    ('=', (0, 255, 0)),
    ('1', (0, 0, 255)),
    ('2', (0, 255, 255)),
    ('3', (255, 0, 255)),
)


def convert(srcfile, dstfile):
    src = Image.open(srcfile)
    dst = open(dstfile, 'w')

    dst.write(str(src.size[0]) + ' ' + str(src.size[1]) + '\n')
    for y in range(src.size[1]):
        for x in range(src.size[0]):
            c = src.getpixel((x, y))
            for char, color in ELEMENTS:
                if color == c:
                    dst.write(char)
                    break
            else:
                print('Unknown pixel', c)
                os.remove(dstfile)
                sys.exit(1)
        dst.write('\n')
    dst.close()


def convert_back(srcfile, dstfile):
    src = open(srcfile, 'r')

    sizeline = src.readline()
    regex = re.compile('\d+')
    size = regex.findall(sizeline)
    if len(size) != 2:
        print('Invalid size', sizeline)
        sys.exit(1)
    width = int(size[0])
    height = int(size[1])

    dst = Image.new('RGB', (width, height))

    for y in range(height):
        for x in range(width):
            c = src.read(1)
            for char, color in ELEMENTS:
                if char == c:
                    dst.putpixel((x, y), color)
                    break
            else:
                print('Unknown character', c)
                sys.exit(1)
        src.read(1)  # \n

    dst.save(dstfile)


if __name__ == '__main__':
    if sys.argv[1].endswith('.png'):
        convert(sys.argv[1], sys.argv[2])
    elif sys.argv[1].endswith('.txt'):
        convert_back(sys.argv[1], sys.argv[2])

