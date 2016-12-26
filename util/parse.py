# -*- coding: utf-8 -*-
from __future__ import print_function

from util.encode import *
from util.encode_dict import *

OPERAND_ENCODE_WIDTH = 50


def set_imm(input_list, encode):
    if len(input_list) == OPERAND_ENCODE_WIDTH:
        encode_len = len(encode)
        if encode_len < 32:
            encode = '0' * (32 - encode_len) + encode
        input_list[OPERAND_ENCODE_WIDTH-50:OPERAND_ENCODE_WIDTH-18] = encode


def set_d(input_list, encode):
    if len(input_list) == OPERAND_ENCODE_WIDTH:
        input_list[OPERAND_ENCODE_WIDTH-18:OPERAND_ENCODE_WIDTH-12] = encode


def set_a(input_list, encode):
    if len(input_list) == OPERAND_ENCODE_WIDTH:
        input_list[OPERAND_ENCODE_WIDTH-12:OPERAND_ENCODE_WIDTH-6] = encode


def set_b(input_list, encode):
    if len(input_list) == OPERAND_ENCODE_WIDTH:
        input_list[OPERAND_ENCODE_WIDTH-6:OPERAND_ENCODE_WIDTH] = encode


def set_a_imm(imm, input_list, encode):
    if imm:
        return set_imm(input_list, encode)
    else:
        return set_a(input_list, encode)


def set_b_imm(imm, input_list, encode):
    if imm:
        return set_imm(input_list, encode)
    else:
        return set_b(input_list, encode)


def parse_aux_reg(input_str):
    ret = None
    if check_aux_reg_name(input_str):
        ret = aux_reg_encode(input_str, aux_reg_encode_dict)
    return ret


def parse_mem_data_addr(input_str, data_dict):
    ret = None
    # mem_data_name = input_str[2:-1]
    mem_data_name = input_str[1:]
    if mem_data_name in data_dict:
        ret = data_dict[mem_data_name]
    return ret


def parse_imm(input_str, data_dict=None):
    ret = None
    if check_mem_data_name(input_str) and data_dict:
        input_str = parse_mem_data_addr(input_str, data_dict)
        if input_str is None:
            raise AsmException('mem addr encode error')

    if check_hex(input_str):
        ret = imm_encode(input_str, 'hex')
    elif check_int(input_str):
        ret = imm_encode(input_str, 'int')
    elif check_bin(input_str):
        ret = imm_encode(input_str, 'bin')
    elif check_num(input_str):
        ret == imm_encode(input_str, 'num')
    return ret


def parse_j_imm(input_str, pc, tag_dict):
    ret = None
    if input_str in tag_dict:
        input_str = '{}'.format(pc - tag_dict[input_str])
        ret = parse_imm(input_str)
    return ret


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


def parse_reg_imm(imm, data_dict, input_str, reg_type_list):
    if imm:
        return parse_imm(input_str, data_dict)
    else:
        return parse_reg(input_str, reg_type_list)


def parse_opcode(opcode):
    if opcode in opcode_encode_dict:
        meta = opcode_encode_dict[opcode]
        return meta['function'] + meta['imm'] + meta['group']
    else:
        print("'{}' is not a valid opcode".format(opcode))
        raise AsmException('opcode parse error')


def parse_000_0(operand, pc, tag_pc_dict):
    ret = ['0'] * OPERAND_ENCODE_WIDTH
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
    ret = ['0'] * OPERAND_ENCODE_WIDTH
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
    ret = ['0'] * OPERAND_ENCODE_WIDTH
    encode0 = None
    encode1 = None
    encode2 = None
    if len(operand) == 3:
        encode0 = parse_reg(operand[0], ['sr'])
        encode1 = parse_reg(operand[1], ['sr'])
        encode2 = parse_reg_imm(imm, data_dict, operand[2], ['sr'])
    if encode0 and encode1 and encode2:
        set_d(ret,encode0)
        set_a(ret, encode1)
        set_b_imm(imm, ret, encode2)
    else:
        raise AsmException("operand parse error")
    return ret


def parse_000_4(imm, operand, data_dict=None):
    ret = ['0'] * OPERAND_ENCODE_WIDTH
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


def parse_001_0(imm, operand, data_dict=None):
    ret = ['0'] * OPERAND_ENCODE_WIDTH
    encode0 = None
    encode1 = None
    if len(operand) == 2:
        encode0 = parse_aux_reg(operand[0])
        if imm:
            encode1 = parse_imm(operand[1], data_dict)
        else:
            encode1 = parse_reg(operand[1], ['sr'])
    if encode0 and encode1:
        set_d(ret, encode0)
        if imm:
            set_imm(ret, encode1)
        else:
            set_a(ret, encode1)
    else:
        raise AsmException("operand parse error")
    return ret


def parse_001_1(imm, operand, data_dict=None):
    ret = ['0'] * OPERAND_ENCODE_WIDTH
    encode0 = None
    encode1 = None
    if len(operand) == 2:
        encode0 = parse_reg(operand[0], ['sr'])
        encode1 = parse_aux_reg(operand[1])
    if encode0 and encode1:
        set_d(ret, encode0)
        set_imm(ret, encode1)
    else:
        raise AsmException("operand parse error")
    return ret


def parse_010_0(imm, operand, data_dict=None):
    ret = ['0'] * OPERAND_ENCODE_WIDTH
    encode0 = None
    encode1 = None
    encode2 = None
    if len(operand) == 3:
        encode0 = parse_reg(operand[0], ['vr', 'vs', 'pr'])
        encode1 = parse_reg(operand[1], ['sr'])
        encode2 = parse_reg_imm(imm, data_dict, operand[2], ['sr'])
    if encode0 and encode1 and encode2:
        set_d(ret, encode0)
        set_a(ret, encode1)
        set_b_imm(imm, ret, encode2)
    else:
        raise AsmException("operand parse error")
    return ret


def parse_011_0(imm, operand, data_dict=None):
    ret = ['0'] * OPERAND_ENCODE_WIDTH
    encode0 = None
    encode1 = None
    encode2 = None
    if len(operand) == 3:
        encode0 = parse_reg(operand[0], ['vr'])
        encode1 = parse_reg(operand[1], ['sr'])
        encode2 = parse_reg(operand[2], ['sr'])
    if encode0 and encode1 and encode2:
        set_d(ret, encode0)
        set_a(ret, encode1)
        set_b(ret, encode2)
    else:
        raise AsmException("operand parse error")
    return ret


def parse_100_0(imm, operand, data_dict=None):
    ret = ['0'] * OPERAND_ENCODE_WIDTH
    encode0 = None
    encode1 = None
    if len(operand) == 2:
        a_encode_list = ['vr', 'vs', 'sr']
        if operand[0] == 'pr':
            a_encode_list.remove('vs')
        encode0 = parse_reg(operand[0], ['vr', 'vs', 'pr'])
        if imm:
            encode1 = parse_imm(operand[1], data_dict)
        else:
            encode1 = parse_reg(operand[1], a_encode_list)
    if encode0 and encode1:
        set_d(ret, encode0)
        if imm:
            set_imm(ret, encode1)
        else:
            set_a(ret, encode1)
    else:
        raise AsmException("operand parse error")
    return ret


def parse_100_1(imm, operand, data_dict=None):
    ret = ['0'] * OPERAND_ENCODE_WIDTH
    encode0 = None
    encode1 = None
    if len(operand) == 2:
        encode0 = parse_reg(operand[0], ['vr', 'pr'])
        encode1 = parse_reg(operand[1], ['vr', 'vs'])
    if encode0 and encode1:
        set_d(ret, encode0)
        set_a(ret, encode1)
    else:
        raise AsmException("operand parse error")
    return ret


def parse_100_2(imm, operand, data_dict=None):
    ret = ['0'] * OPERAND_ENCODE_WIDTH
    encode0 = None
    encode1 = None
    if len(operand) == 2:
        encode0 = parse_reg(operand[0], ['vr', 'vs'])
        encode1 = parse_reg(operand[1], ['vr', 'pr'])
    if encode0 and encode1:
        set_d(ret, encode0)
        set_a(ret, encode1)
    else:
        raise AsmException("operand parse error")
    return ret


def parse_101_0(imm, operand, data_dict=None):
    ret = ['0'] * OPERAND_ENCODE_WIDTH
    encode0 = None
    encode1 = None
    encode2 = None
    if len(operand) == 3:
        encode0 = parse_reg(operand[0], ['vr'])
        encode1 = parse_reg(operand[1], ['vr'])
        if imm:
            encode2 = parse_imm(operand[2], data_dict)
        else:
            encode2 = parse_reg(operand[2], ['vr', 'sr'])
    if encode0 and encode1 and encode2:
        set_d(ret, encode0)
        set_a(ret, encode1)
        if imm:
            set_imm(ret, encode2)
        else:
            set_b(ret, encode2)
    else:
        raise AsmException("operand parse error")
    return ret


def parse_101_1(imm, operand, data_dict=None):
    ret = ['0'] * OPERAND_ENCODE_WIDTH
    encode0 = None
    encode1 = None
    if len(operand) == 2:
        encode0 = parse_reg(operand[0], ['vr', 'pr'])
        encode1 = parse_reg(operand[1], ['vr'])
    if encode0 and encode1:
        set_d(ret, encode0)
        set_a(ret, encode1)
    else:
        raise AsmException("operand parse error")
    return ret


def parse_101_2(imm, operand, data_dict=None):
    ret = ['0'] * OPERAND_ENCODE_WIDTH
    encode0 = None
    encode1 = None
    encode2 = None
    if len(operand) == 3:
        encode0 = parse_reg(operand[0], ['vr'])
        encode1 = parse_reg(operand[1], ['vr'])
        if imm:
            encode2 = parse_imm(operand[2], data_dict)
        else:
            encode2 = parse_reg(operand[2], ['sr'])
    if encode0 and encode1 and encode2:
        set_d(ret, encode0)
        set_a(ret, encode1)
        if imm:
            set_imm(ret, encode2)
        else:
            set_b(ret, encode2)
    else:
        raise AsmException("operand parse error")
    return ret


def parse_101_3(imm, operand, data_dict=None):
    ret = ['0'] * OPERAND_ENCODE_WIDTH
    encode0 = None
    encode1 = None
    encode2 = None
    if len(operand) == 3:
        encode0 = parse_reg(operand[0], ['vr', 'pr'])
        encode1 = parse_reg(operand[1], ['vr'])
        encode2 = parse_reg(operand[2], ['vr', 'vs'])
    if encode0 and encode1 and encode2:
        set_d(ret, encode0)
        set_a(ret, encode1)
        set_b(ret, encode2)
    else:
        raise AsmException("operand parse error")
    return ret


def parse_101_4(imm, operand, data_dict=None):
    ret = ['0'] * OPERAND_ENCODE_WIDTH
    encode0 = None
    encode1 = None
    if len(operand) == 2:
        encode0 = parse_reg(operand[0], ['vr'])
        encode1 = parse_reg(operand[1], ['vr'])
    if encode0 and encode1:
        set_d(ret, encode0)
        set_a(ret, encode1)
    else:
        raise AsmException("operand parse error")
    return ret


def parse_110_0(imm, operand, data_dict=None):
    ret = ['0'] * OPERAND_ENCODE_WIDTH
    encode0 = None
    encode1 = None
    encode2 = None
    if len(operand) == 3:
        encode0 = parse_reg(operand[0], ['vr'])
        encode1 = parse_reg(operand[1], ['vr'])
        encode2 = parse_reg(operand[2], ['vr', 'vs'])
    if encode0 and encode1 and encode2:
        set_d(ret, encode0)
        set_a(ret, encode1)
        set_b(ret, encode2)
    else:
        raise AsmException("operand parse error")
    return ret


def parse_110_1(imm, operand, data_dict=None):
    ret = ['0'] * OPERAND_ENCODE_WIDTH
    encode0 = None
    encode1 = None
    encode2 = None
    if len(operand) == 3:
        encode0 = parse_reg(operand[0], ['vr'])
        encode1 = parse_reg(operand[1], ['vr'])
        encode2 = parse_reg(operand[2], ['vs'])
    if encode0 and encode1 and encode2:
        set_d(ret, encode0)
        set_a(ret, encode1)
        set_b(ret, encode2)
    else:
        raise AsmException("operand parse error")
    return ret


def parse_110_2(imm, operand, data_dict=None):
    ret = ['0'] * OPERAND_ENCODE_WIDTH
    encode0 = None
    encode1 = None
    if len(operand) == 2:
        encode0 = parse_reg(operand[0], ['vr'])
        encode1 = parse_reg(operand[1], ['vr'])
    if encode0 and encode1:
        set_d(ret, encode0)
        set_a(ret, encode1)
    else:
        raise AsmException("operand parse error")
    return ret


def parse_111_0(imm, operand, data_dict=None):
    ret = ['0'] * OPERAND_ENCODE_WIDTH
    encode0 = None
    encode1 = None
    encode2 = None
    if len(operand) == 3:
        encode0 = parse_reg(operand[0], ['vr'])
        encode1 = parse_reg(operand[1], ['vr'])
        if imm:
            encode2 = parse_imm(operand[2], data_dict)
        else:
            encode2 = parse_reg(operand[2], ['vr', 'sr'])
    if encode0 and encode1 and encode2:
        set_d(ret, encode0)
        set_a(ret, encode1)
        if imm:
            set_imm(ret, encode2)
        else:
            set_b(ret, encode2)
    else:
        raise AsmException("operand parse error")
    return ret


def parse_111_1(imm, operand, data_dict=None):
    ret = ['0'] * OPERAND_ENCODE_WIDTH
    encode0 = None
    encode1 = None
    encode2 = None
    if len(operand) == 3:
        encode0 = parse_reg(operand[0], ['vr'])
        encode1 = parse_reg(operand[1], ['vr'])
        if imm:
            encode2 = parse_imm(operand[2], data_dict)
        else:
            encode2 = parse_reg(operand[2], ['sr'])
    if encode0 and encode1 and encode2:
        set_d(ret, encode0)
        set_a(ret, encode1)
        if imm:
            set_imm(ret, encode2)
        else:
            set_b(ret, encode2)
    else:
        raise AsmException("operand parse error")
    return ret


def parse_operand(op_type, imm, operand, pc, tag_pc_dict, data_offset_dict):
    ret = ['0'] * OPERAND_ENCODE_WIDTH
    if op_type == '000_0':
        ret = parse_000_0(operand, pc, tag_pc_dict)
    elif op_type == '000_1':
        ret = parse_000_1(operand, pc, tag_pc_dict)
    elif op_type == '000_2':
        pass
    elif op_type == '000_3':
        ret = parse_000_3(imm, operand, data_offset_dict)
    elif op_type == '000_4':
        ret = parse_000_4(imm, operand, data_offset_dict)
    elif op_type == '001_0':
        ret = parse_001_0(imm, operand, data_offset_dict)
    elif op_type == '001_1':
        ret = parse_001_1(imm, operand, data_offset_dict)
    elif op_type == '010_0':
        ret = parse_010_0(imm, operand, data_offset_dict)
    elif op_type == '011_0':
        ret = parse_011_0(imm, operand, data_offset_dict)
    elif op_type == '100_0':
        ret = parse_100_0(imm, operand, data_offset_dict)
    elif op_type == '100_1':
        ret = parse_100_1(imm, operand, data_offset_dict)
    elif op_type == '100_2':
        ret = parse_100_2(imm, operand, data_offset_dict)
    elif op_type == '101_0':
        ret = parse_101_0(imm, operand, data_offset_dict)
    elif op_type == '101_1':
        ret = parse_101_1(imm, operand, data_offset_dict)
    elif op_type == '101_2':
        ret = parse_101_2(imm, operand, data_offset_dict)
    elif op_type == '101_3':
        ret = parse_101_3(imm, operand, data_offset_dict)
    elif op_type == '101_4':
        ret = parse_101_4(imm, operand, data_offset_dict)
    elif op_type == '110_0':
        ret = parse_110_0(imm, operand, data_offset_dict)
    elif op_type == '110_1':
        ret = parse_110_1(imm, operand, data_offset_dict)
    elif op_type == '110_2':
        ret = parse_110_2(imm, operand, data_offset_dict)
    elif op_type == '111_0':
        ret = parse_111_0(imm, operand, data_offset_dict)
    elif op_type == '111_1':
        ret = parse_111_1(imm, operand, data_offset_dict)
    return ret


def parse_code(opcode, operand, pc, tag_pc_dict, data_offset_dict):
    ret = ['0'] * 64
    ret[-12:] = parse_opcode(opcode)
    op_type = opcode_encode_dict[opcode]['type']
    imm = bool(int(opcode_encode_dict[opcode]['imm']))
    # TODO encode confuse
    if op_type in ['000_3', '010_0']:
        imm = imm or check_mem_data_name(operand[2])
        ret[-4] = str(int(imm))
    ret[2:-12] = \
        parse_operand(op_type, imm, operand, pc, tag_pc_dict, data_offset_dict)
    return ret
