# -*- coding: utf-8 -*-
from util.decode import *


def get_operand_imm_bits(input_str):
    return input_str[2:34]


def get_operand_reg_bits(input_str):
    return input_str[34:52]


def get_function_bits(input_str):
    return input_str[52:60]


def get_imm_bits(input_str):
    return input_str[60:61]


def get_group_bits(input_str):
    return input_str[61:]


def disassemble(input_str):
    ret = None
    opcode = ''
    operand_imm = ''
    operand_reg = ''
    operand_imm_bits = get_operand_imm_bits(input_str)
    operand_reg_bits = get_operand_reg_bits(input_str)
    function_bits = get_function_bits(input_str)
    imm_bits = get_imm_bits(input_str)
    group_bits = get_group_bits(input_str)

    fun_imm_group_pair = function_bits + '_' + imm_bits + '_' + group_bits
    opcode = decode_opcode(fun_imm_group_pair)

    if bool(imm_bits):
        if opcode == 's_rauxi':
            operand_imm = decode_aux_reg(operand_imm_bits[-6:])
        else:
            operand_imm = decode_imm(operand_imm_bits)

    if opcode in ['s_raux', 's_rauxi']:
        pass



if __name__ == '__main__':
    pass
