# -*- coding: utf-8 -*-
import re
from exception_util import AsmException
from encode_dict import *


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


def check_aux_reg_name(check_input):
    aux_reg_pattern = re.compile(r'\[\w+\]$')
    match = aux_reg_pattern.match(str(check_input))
    if match:
        return True
    return False


def hex2bin(input_num, truncate=None):
    if isinstance(input_num, str):
        int_num = int(input_num, 16)
    else:
        int_num = int(input_num)
    ret = int2bin(int_num, truncate)
    return ret


def int2bin(input_num, truncate=None):
    ret = '{:0>64b}'.format(
            (int(input_num) + 0x10000000000000000) & 0xffffffffffffffff)
    if truncate:
        ret = ret[-truncate:]
    return ret


def imm_encode(imm, base):
    ret = None
    if base == 'hex':
        ret = hex2bin(imm, 32)
    elif base == 'int':
        ret = int2bin(imm, 32)
    return ret


def mem_data_addr_encode(input_str, data_dict):
    ret = None
    mem_data_name = input_str[2:-1]
    if mem_data_name in data_dict:
        ret = int2bin(data_dict[mem_data_name])
    return ret


def reg_encode(input_str, reg_dict):
    ret = None
    if input_str in reg_dict:
        ret = reg_dict[input_str]
    return ret


def aux_reg_encode(input_str, reg_dict):
    ret = None
    aux_reg_name = input_str[1:-1]
    if aux_reg_name in reg_dict:
        ret = hex2bin(reg_dict[aux_reg_name], truncate=8)
    return ret
