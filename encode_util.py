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


def check_mem_data_name(check_input):
    mem_data_pattern = re.compile(r'\$\(\w+\)$')
    match = mem_data_pattern.match(str(check_input))
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


def imm_encode(imm, base):
    ret = None
    if base == 'hex':
        ret = hex2bin(imm)
    elif base == 'int':
        ret = int2bin(imm)
    else:
        raise AsmException('immediate encode error')
    return ret


def mem_data_addr_encode(input_str, data_dict):
    ret = None
    mem_data_name = input_str[2:-1]
    if mem_data_name in data_dict:
        ret = int2bin(data_dict[mem_data_name])
    else:
        raise AsmException('memory data address encode error')
    return ret
