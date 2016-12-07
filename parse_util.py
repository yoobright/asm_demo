# -*- coding: utf-8 -*-
from encode_dict import reg_encode_dict
from encode_dict import opcode_encode_dict


def parse_s_j0(opcode, operand, tag_pc_dict, data_offset_dict):
    pass


def parse_s_j1(op_ode, operand, tag_pc_dict, data_offset_dict):
    pass


def parse_s_j2(opcode, operand, tag_pc_dict, data_offset_dict):
    pass


def parse_s_a0(opcode, operand, tag_pc_dict, data_offset_dict):
    pass


def parse_s_a1(opcode, operand, tag_pc_dict, data_offset_dict):
    pass


def parse_s_s0(opcode, operand, tag_pc_dict, data_offset_dict):
    pass


def parse_s_p0(opcode, operand, tag_pc_dict, data_offset_dict):
    pass


def parse_s_m0(opcode, operand, tag_pc_dict, data_offset_dict):
    pass


def parse_v_p0(opcode, operand, tag_pc_dict, data_offset_dict):
    pass


def parse_code(opcode, operand, tag_pc_dict, data_offset_dict):
    op_type = opcode_encode_dict[opcode][1]
    if op_type == 's_j0':
        return parse_s_j0(opcode, operand, tag_pc_dict, data_offset_dict)
    elif op_type == 's_j1':
        return parse_s_j1(opcode, operand, tag_pc_dict, data_offset_dict)
    elif op_type == 's_j2':
        return parse_s_j2(opcode, operand, tag_pc_dict, data_offset_dict)
    elif op_type == 's_a0':
        return parse_s_a0(opcode, operand, tag_pc_dict, data_offset_dict)
    elif op_type == 's_a1':
        return parse_s_a1(opcode, operand, tag_pc_dict, data_offset_dict)
    elif op_type == 's_s0':
        return parse_s_s0(opcode, operand, tag_pc_dict, data_offset_dict)
    elif op_type == 's_p0':
        return parse_s_p0(opcode, operand, tag_pc_dict, data_offset_dict)
    elif op_type == 's_m0':
        return parse_s_m0(opcode, operand, tag_pc_dict, data_offset_dict)
    elif op_type == 'v_p0':
        return parse_v_p0(opcode, operand, tag_pc_dict, data_offset_dict)