# -*- coding: utf-8 -*-
import re
import sys
import numpy as np
from exception import AsmException
from deModel import DeFixedInt


def is_string(s):
    # if we use Python 3
    if sys.version_info[0] >= 3:
        return isinstance(s, str)
    # we use Python 2
    return isinstance(s, basestring)


def check_hex(check_input):
    hex_pattern = re.compile(r'0x[0-9a-fA-F]+$')
    match = hex_pattern.match(str(check_input))
    if match:
        return True
    return False


def check_int(check_input):
    int_pattern = re.compile(r'[-+]?[0-9]+$')
    match = int_pattern.match(str(check_input))
    if match:
        return True
    return False


def check_num(check_input):
    num_pattern = re.compile(r'[-+]?[0-9]*\.?[0-9]+$')
    match = num_pattern.match(str(check_input))
    if match:
        return True
    return False


def check_bin(check_input):
    bin_pattern = re.compile(r'0b([01]+|[01]+_)*[01]+$')
    match = bin_pattern.match(str(check_input))
    if match:
        return True
    return False


def check_mem_data_name(check_input):
    # mem_data_pattern = re.compile(r'\$\(\w+\)$')
    mem_data_pattern = re.compile(r'\$\w+$')
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


def bin2bin(input_num, truncate=None):
    int_num = None
    if is_string(input_num):
        input_num = input_num.replace("_", "")
        int_num = int(input_num, 2)
    ret = int2bin(int_num, truncate)
    return ret


def int2bin(input_num, truncate=None):
    ret = '{:0>64b}'.format(
            (int(input_num) + 0x10000000000000000) & 0xffffffffffffffff)
    if truncate:
        ret = ret[-truncate:]
    return ret


def single2bin(input_num, truncate=32):
    if is_string(input_num):
        input_num = eval(input_num)
    ret = np.binary_repr(np.float32(input_num).view(np.int32), truncate)
    return ret


def fix322bin(input_num, fraction=None):
    if is_string(input_num):
        input_num = eval(input_num)
    if fraction is None:
        fraction = 8
    if fraction > 31:
        raise AsmException('fraction out of range')
    int_w = 32 - fraction - 1
    ret = DeFixedInt(int_w, fraction, input_num).bit()
    return ret


def fix162bin(input_num, fraction=None):
    if is_string(input_num):
        input_num = eval(input_num)
    if fraction is None:
        fraction = 8
    if fraction > 15:
        raise AsmException('fraction out of range')
    int_w = 16 - fraction - 1
    ret = DeFixedInt(int_w, fraction, input_num).bit()
    return ret


def fix82bin(input_num, fraction=None):
    if is_string(input_num):
        input_num = eval(input_num)
    if fraction is None:
        fraction = 4
    if fraction > 7:
        raise AsmException('fraction out of range')
    int_w = 8 - fraction - 1
    ret = DeFixedInt(int_w, fraction, input_num).bit()
    return ret


def fix42bin(input_num, fraction=None):
    if is_string(input_num):
        input_num = eval(input_num)
    if fraction is None:
        fraction = 2
    if fraction > 3:
        raise AsmException('fraction out of range')
    int_w = 4 - fraction - 1
    ret = DeFixedInt(int_w, fraction, input_num).bit()
    return ret


def imm_encode(imm, base):
    ret = None
    if base == 'hex':
        ret = hex2bin(imm, 32)
    elif base == 'int':
        ret = int2bin(imm, 32)
    elif base == 'bin':
        ret = bin2bin(imm, 32)
    return ret


def dtype_encode(input_str, dtype, fraction):
    ret = None
    if dtype == 'w':
        ret = single2bin(input_str)

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
        ret = reg_dict[aux_reg_name]
    return ret
