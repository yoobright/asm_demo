# -*- coding: utf-8 -*-
from __future__ import print_function
from encode_dict import reg_encode_dict
from encode_dict import aux_reg_encode_dict
from encode_dict import opcode_encode_dict


reg_decode_dict = {}
for key, value in reg_encode_dict.items():
    reg_decode_dict[value] = key

aux_reg_decode_dict = {}
for key, value in aux_reg_encode_dict.items():
    aux_reg_decode_dict[value] = key

opcode_decode_dict = {}
for key, value in opcode_encode_dict.items():
    fun_imm_group_pair = opcode_encode_dict[key]['function'] + '_' + \
        opcode_encode_dict[key]['imm'] + '_' + \
        opcode_encode_dict[key]['group']
    opcode_decode_dict[fun_imm_group_pair] = {
        'opcode': key,
        'operand_num': opcode_encode_dict[key]['operand_num']
    }


if __name__ == '__main__':
    print(reg_decode_dict)
    print(aux_reg_decode_dict)
    print(opcode_decode_dict)
