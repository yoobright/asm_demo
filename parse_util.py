# -*- coding: utf-8 -*-
from __future__ import print_function
from encode_dict import reg_encode_dict
from encode_dict import opcode_encode_dict
from exception_util import AsmException
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


def parse_opcode(opcode):
    if opcode in opcode_encode_dict:
        meta = opcode_encode_dict[opcode]
        return meta['function'] + meta['imm'] + meta['group']
    else:
        print("'{}' is not a valid opcode".format(opcode))
        raise AsmException('opcode parse error')


def parse_operand(op_type, operand, tag_pc_dict, data_offset_dict):
    ret = ['0'] * 50
    return ret


def parse_code(opcode, operand, tag_pc_dict, data_offset_dict):
    ret = ['0'] * 64
    print(opcode)
    ret[-12:] = parse_opcode(opcode)
    op_type = opcode_encode_dict[opcode]['type']
    ret[2:-12] = parse_operand(op_type, operand, tag_pc_dict, data_offset_dict)
    return ret
