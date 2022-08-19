import random

import numpy as np
import copy


def gen(list_item):
    for m in list_item:
        yield m


def shuffle(data):
    index = np.arange(len(data))
    np.random.shuffle(index)
    a = list(np.array(data)[index])
    return a, list(index+1)


def appendgen(gen, alist):
    tmp = copy.deepcopy(gen)
    return [i for i in tmp]


def rgb2colname(r, g, b):
    rh, gh, bh = (hex(r)[2:], hex(b)[2:], hex(b)[2:])
    if len(rh) == 1:
        rh = '0' + rh
    if len(gh) == 1:
        gh = '0' + gh
    if len(bh) == 1:
        bh = '0' + bh
    return '#' + rh + gh + bh


def color_enum(start, step, num):
    r, g, b = start
    rs, gs, bs = step
    color_set = list()
    for i in range(0, num):
        rc, gc, bc = r + i * rs, g + i * gs, b + i * bs
        c = rgb2colname(rc, gc, bc)
        color_set.append(c)
    return color_set


if __name__ == '__main__':
    shuffle(['c','r','d','k','i'])