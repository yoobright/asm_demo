# -*- coding: utf-8 -*-
from encode_dict import reg_encode_dict
from encode_dict import opcode_encode_dict
from encode_util import *


def parse_imm(input_str):
    if check_hex(input_str):
        return imm_encode(input_str, 'hex')
    if check_int(input_str):
        return imm_encode(input_str, 'int')


def parse_j_imm(input_str, tag_list, pc):
    if input_str in tag_list:
        input_str = '{}'.format(pc - tag_list[input_str])
    return parse_imm(input_str)




def parse_code(opcode, operand, tag_pc_dict, data_offset_dict):
    ret = ['0'] * 64
    return ret
