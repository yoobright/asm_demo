# -*- coding: utf-8 -*-
from decode_dict import reg_decode_dict
from decode_dict import aux_reg_decode_dict
from decode_dict import opcode_decode_dict


def decode_reg(input_str):
    ret = None
    if input_str in reg_decode_dict:
        ret = reg_decode_dict[input_str]
    return ret


def decode_aux_reg(input_str):
    ret = None
    if input_str in aux_reg_decode_dict:
        ret = "[{0}]".format(aux_reg_decode_dict[input_str])
    return ret


def decode_opcode(input_str):
    ret = None
    if input_str in opcode_decode_dict:
        ret = opcode_decode_dict[input_str]['opcode']
    return ret


def decode_operand_num(input_str):
    ret = None
    if input_str in opcode_decode_dict:
        ret = opcode_decode_dict[input_str]['operand_num']
    return ret


def decode_3_reg(input_str):
    d_bits = input_str[0:6]
    a_bits = input_str[6:12]
    b_bits = input_str[12:]

    d_decode = decode_reg(d_bits)
    a_decode = decode_reg(a_bits)
    b_decode = decode_reg(b_bits)

    decode_list = filter(lambda x: x, [d_decode, a_decode, b_decode])
    ret = ' '.join(decode_list).strip()

    return ret


def decode_2_reg(input_str):
    d_bits = input_str[0:6]
    a_bits = input_str[6:12]

    d_decode = decode_reg(d_bits)
    a_decode = decode_reg(a_bits)

    decode_list = filter(lambda x: x, [d_decode, a_decode])
    ret = ' '.join(decode_list).strip()

    return ret


def decode_1_reg(input_str):
    d_bits = input_str[0:6]

    d_decode = decode_reg(d_bits)

    decode_list = filter(lambda x: x, [d_decode])
    ret = ' '.join(decode_list).strip()

    return ret


def decode_imm(input_str):
    ret = hex(int(input_str, 2) + 0x100000000)
    ret = ret[0:2] + ret[3:-1]
    return ret
