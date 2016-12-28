# -*- coding: utf-8 -*-
from util.decode import *
from util.exception import DasmException
import re


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


def check_input_str(input_str):
    p = re.compile(r'[01]{64}')
    match = p.match(input_str)
    if not match:
        raise DasmException('input string is not valid')


def disassemble(input_str):
    input_str = input_str.replace('_', '')
    check_input_str(input_str)
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
    operand_num = decode_operand_num(fun_imm_group_pair)

    if bool(imm_bits):
        if opcode == 's_rauxi':
            operand_imm = decode_aux_reg(operand_imm_bits[-6:])
        else:
            operand_imm = decode_imm(operand_imm_bits)

        if opcode == 's_wauxi':
            operand_reg = decode_aux_reg(operand_reg_bits[0:6])
        else:
            if operand_num == 3:
                operand_reg = decode_2_reg(operand_reg_bits)
            elif operand_reg == 2:
                operand_reg = decode_1_reg(operand_reg_bits)
    else:
        if opcode == 's_waux':
            operand_reg = decode_aux_reg(operand_reg_bits[0:6]) + ' ' + \
                decode_reg(operand_reg_bits[6:12])
        else:
            if operand_num == 3:
                operand_reg = decode_3_reg(operand_reg_bits)
            elif operand_reg == 2:
                operand_reg = decode_2_reg(operand_reg_bits)
            elif operand_reg == 1:
                operand_reg = decode_1_reg(operand_reg_bits)
            elif operand_reg == 0:
                pass
    op_list = filter(lambda x: x != '', [opcode, operand_reg, operand_imm])
    ret = ' '.join(op_list)
    return ret




if __name__ == '__main__':
    pass
