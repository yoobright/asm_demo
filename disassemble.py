# -*- coding: utf-8 -*-
import argparse
import re
from util.decode import *
from util.exception import DasmException

code_list = []


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

    if imm_bits == '1':
        if opcode == 's_rauxi':
            operand_imm = decode_aux_reg(operand_imm_bits[-6:])
        else:
            operand_imm = decode_imm(operand_imm_bits)

        if opcode in ['s_bne', 's_beq', 's_blt', 's_bltu', 's_bge', 's_bgeu']:
            operand_imm = '{}'.format(bin2signed_int(operand_imm_bits))

        if opcode == 's_wauxi':
            operand_reg = decode_aux_reg(operand_reg_bits[0:6])
        else:
            if operand_num == 3:
                operand_reg = decode_2_reg(operand_reg_bits)
            elif operand_num == 2:
                operand_reg = decode_1_reg(operand_reg_bits)
    else:
        if opcode == 's_waux':
            operand_reg = decode_aux_reg(operand_reg_bits[0:6]) + ' ' + \
                decode_reg(operand_reg_bits[6:12])
        else:
            if operand_num == 3:
                operand_reg = decode_3_reg(operand_reg_bits)
            elif operand_num == 2:
                operand_reg = decode_2_reg(operand_reg_bits)
            elif operand_num == 1:
                operand_reg = decode_1_reg(operand_reg_bits)
            elif operand_num == 0:
                pass
    if not opcode:
        raise DasmException('can not disassemble opcode')
    op_list = filter(lambda x: x != '', [opcode, operand_reg, operand_imm])
    if len(op_list) == 1:
        ret = op_list[0]
    else:
        list_tmp = ' '.join(op_list).split()
        ret = list_tmp[0] + ' ' + ', '.join(list_tmp[1:])
    return ret


def main():
    if input_file:
        with open(input_file, 'r') as in_f:
            for file_line in in_f.readlines():
                code = disassemble(file_line.strip())
                if code:
                    code_list.append(code)

    if verbose:
        for code in code_list:
            print(code)

    if output_file:
        with open(output_file, 'w') as out_f:
            for code in code_list:
                out_f.write('{0}\n'.format(code))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, default=None,
                        help="input file name")
    parser.add_argument('-o', '--output', type=str, default=None,
                        help="output file name")
    parser.add_argument("-v", '--verbose', action="store_true",
                        help="increase output verbosity")
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output
    verbose = args.verbose

    # input_file = "test\\dtest.txt"
    # verbose = True
    main()