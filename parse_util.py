# -*- coding: utf-8 -*-
from __future__ import print_function
from encode_dict import sr_encode_dict
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


def parse_reg(input_str, reg_type_list):
    ret = None
    reg_list = []
    if 'sr' in reg_type_list:
        reg_list += sr_encode_dict.items()
    if 'vr' in reg_type_list:
        reg_list += vr_encode_dict.items()
    if 'vs' in reg_type_list:
        reg_list += vs_encode_dict.items()
    if 'pr' in reg_type_list:
        reg_list += pr_encode_dict.items()
    if reg_list:
        reg_dict = dict(reg_list)
        ret = reg_encode(input_str, reg_dict)
    return ret


def parse_opcode(opcode):
    if opcode in opcode_encode_dict:
        meta = opcode_encode_dict[opcode]
        return meta['function'] + meta['imm'] + meta['group']
    else:
        print("'{}' is not a valid opcode".format(opcode))
        raise AsmException('opcode parse error')


def parse_000_0(imm, operand, tag_pc_dict, data_offset_dict):
    ret = ['0'] * 50
    encode1 = None
    encode2 = None
    encode3 = None
    # if len(operand) == 3:
    return ret


def parse_operand(op_type, imm, operand, tag_pc_dict, data_offset_dict):
    ret = ['0'] * 50
    if op_type == '000_0':
        ret = parse_000_0(imm, operand, tag_pc_dict, data_offset_dict)
    return ret


def parse_code(opcode, operand, tag_pc_dict, data_offset_dict):
    ret = ['0'] * 64
    print(opcode)
    ret[-12:] = parse_opcode(opcode)
    op_type = opcode_encode_dict[opcode]['type']
    imm = bool(int(opcode_encode_dict[opcode]['imm']))
    ret[2:-12] = parse_operand(op_type, imm, operand, tag_pc_dict, data_offset_dict)
    return ret
