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


def imm_encode(imm):
    ret = None
    if check_hex(imm):
        ret = '{:0>64b}'.format(
            (int(imm[2:], 16) + 0x10000000000000000) & 0xffffffffffffffff)
    elif check_int(imm):
        ret = '{:0>64b}'.format(
            (int(imm) + 0x10000000000000000) & 0xffffffffffffffff)
    else:
        raise AsmException('immediate check error')
    return ret
