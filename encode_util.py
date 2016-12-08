# -*- coding: utf-8 -*-
import re
from exception_util import AsmException


def check_hex(check_input):
    hex_pattern = re.compile(r'0x[0-9a-fA-F]+$')
    match = hex_pattern.match(str(check_input))
    if match:
        return True
    return False


def check_int(check_input):
    int_pattern = re.compile(r'-*[0-9]+$')
    match = int_pattern.match(str(check_input))
    if match:
        return True
    return False


def hex2bin(input_num):
    if isinstance(input_num, basestring):
        int_num = int(input_num, 16)
    else:
        int_num = int(input_num)
    ret = int2bin(int_num)
    return ret


def int2bin(input_num):
    ret = '{:0>64b}'.format(
            (int(input_num) + 0x10000000000000000) & 0xffffffffffffffff)
    return ret


def imm_encode(imm):
    ret = None
    if check_hex(imm):
        ret = hex2bin(imm)
    elif check_int(imm):
        ret = int2bin(imm)
    else:
        raise AsmException('immediate check error')
    return ret
