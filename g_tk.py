# -*- coding: UTF-8 -*-
import sys

def LongToInt(value):                # 由于int+int超出范围后自动转为long型，通过这个转回来
    if isinstance(value, int):
        return int(value)
    else:
        return int(value & sys.maxint)
def LeftShiftInt(number, step):     # 由于左移可能自动转为long型，通过这个转回来
    if isinstance((number << step), long):
        return int((number << step) - 0x200000000L)
    else:
        return int(number << step)
def getOldGTK(skey):
    a = 5381
    for i in range(0, len(skey)):
        a = a + LeftShiftInt(a, 5) + ord(skey[i])
        a = LongToInt(a)
    return a & 0x7fffffff

def getNewGTK(p_skey, skey, rv2):
    b = p_skey or skey or rv2
    a = 5381
    for i in range(0, len(b)):
        a = a + LeftShiftInt(a, 5) + ord(b[i])
        a = LongToInt(a)
    return a & 0x7fffffff