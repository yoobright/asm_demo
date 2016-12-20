# -*- coding: utf-8 -*-
from __future__ import print_function
from encode_dict import *
# from encode_dict import opcode_encode_dict
from exception_util import AsmException
from encode_util import *


def set_imm(input_list, encode):
    if len(input_list) == 50:
        input_list[0:32] = encode


def set_d(input_list, encode):
    if len(input_list) == 50:
        input_list[32:38] = encode


def set_a(input_list, encode):
    if len(input_list) == 50:
        input_list[38:44] = encode


def set_b(input_list, encode):
    if len(input_list) == 50:
        input_list[44:50] = encode


def parse_mem_data_addr(input_str, data_dict):
    ret = None
    mem_data_name = input_str[2:-1]
    if mem_data_name in data_dict:
        ret = data_dict[mem_data_name]
    return ret


def parse_imm(input_str, data_dict=None):
    ret = None
    if check_mem_data_name(input_str) and data_dict:
        input_str = parse_mem_data_addr(input_str, data_dict)
        if not input_str:
            raise AsmException('mem addr encode error')
    if check_hex(input_str):
        ret = imm_encode(input_str, 'hex')
    elif check_int(input_str):
        ret = imm_encode(input_str, 'int')
    return ret


def parse_j_imm(input_str, pc, tag_dict):
    if input_str in tag_dict:
        input_str = '{}'.format(pc - tag_dict[input_str])
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


def parse_000_0(operand, pc, tag_pc_dict):
    ret = ['0'] * 50
    encode0 = None
    encode1 = None
    encode2 = None
    if len(operand) == 3:
        encode0 = parse_reg(operand[0], ['sr'])
        encode1 = parse_reg(operand[1], ['sr'])
        encode2 = parse_j_imm(operand[2], pc, tag_pc_dict)
    if encode0 and encode1 and encode2:
        set_d(ret, encode0)
        set_a(ret, encode1)
        set_imm(ret, encode2)
    else:
        raise AsmException("operand parse error")
    return ret


def parse_000_1(operand, pc, tag_pc_dict):
    ret = ['0'] * 50
    encode0 = None
    encode1 = None
    encode2 = None
    if len(operand) == 3:
        encode0 = parse_reg(operand[0], ['sr'])
        encode1 = parse_reg(operand[1], ['sr'])
        encode2 = parse_j_imm(operand[2], pc, tag_pc_dict)
    if encode0 and encode1 and encode2:
        set_a(ret, encode0)
        set_b(ret, encode1)
        set_imm(ret, encode2)
    else:
        raise AsmException("operand parse error")
    return ret


def parse_000_3(imm, operand, data_dict=None):
    ret = ['0'] * 50
    encode0 = None
    encode1 = None
    encode2 = None
    if len(operand) == 3:
        encode0 = parse_reg(operand[0], ['sr'])
        encode1 = parse_reg(operand[1], ['sr'])
        if imm:
            encode2 = parse_imm(operand[2], data_dict)
        else:
            encode2 = parse_reg(operand[2], ['sr'])
    if encode0 and encode1 and encode2:
        set_d(ret,encode0)
        set_a(ret, encode1)
        if imm:
            set_imm(ret, encode2)
        else:
            set_b(ret, encode2)
    else:
        raise AsmException("operand parse error")
    return ret


def parse_000_4(imm, operand, data_dict=None):
    ret = ['0'] * 50
    encode0 = None
    encode1 = None
    if len(operand) == 2:
        encode0 = parse_reg(operand[0], ['sr'])
        encode1 = parse_imm(operand[1], data_dict)
    if encode0 and encode1:
        set_d(ret, encode0)
        if imm:
            set_imm(ret, encode1)
    else:
        raise AsmException("operand parse error")
    return ret


def parse_operand(op_type, imm, operand, pc, tag_pc_dict, data_offset_dict):
    ret = ['0'] * 50
    if op_type == '000_0':
        ret = parse_000_0(operand, pc, tag_pc_dict)
    elif op_type == '000_1':
        ret = parse_000_1(operand, pc, tag_pc_dict)
    elif op_type == '000_2':
        pass
    elif op_type == '000_3':
        ret = parse_000_3(imm, operand, data_offset_dict)
    return ret


def parse_code(opcode, operand, pc, tag_pc_dict, data_offset_dict):
    ret = ['0'] * 64
    print(opcode)
    ret[-12:] = parse_opcode(opcode)
    op_type = opcode_encode_dict[opcode]['type']
    imm = bool(int(opcode_encode_dict[opcode]['imm']))
    ret[2:-12] = \
        parse_operand(op_type, imm, operand, pc, tag_pc_dict, data_offset_dict)
    return ret
