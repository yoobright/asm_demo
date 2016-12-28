# -*- coding: utf-8 -*-
from __future__ import print_function

from util.encode import *
from util.encode_dict import *

OPERAND_ENCODE_WIDTH = 50

"""
preprocess:
000_3, 010_0: for load mem data addr
101_0: for multi-type imm
"""


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
    return ret


def parse_j_imm(input_str, pc, tag_dict):
    ret = None
    if input_str in tag_dict:
        input_str = '{}'.format(pc - tag_dict[input_str])
        ret = parse_imm(input_str)
    return ret


def parse_d_imm(input_str, dtype, fraction=None):
    ret = None
    if dtype:
        ret = dtype_encode(input_str, dtype, fraction)
    else:
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


class Factory(object):
    @staticmethod
    def get_parser(opcode):
        op_type = opcode_encode_dict[opcode]['type']
        if op_type == '000_0':
            return Parser_000_0
        elif op_type == '000_1':
            return Parser_000_1
        elif op_type == '000_2':
            return Parser_000_2
        elif op_type == '000_3':
            return Parser_000_3
        elif op_type == '000_4':
            return Parser_000_4
        elif op_type == '001_0':
            return Parser_001_0
        elif op_type == '001_1':
            return Parser_001_1
        elif op_type == '010_0':
            return Parser_010_0
        elif op_type == '011_0':
            return Parser_011_0
        elif op_type == '100_0':
            return Parser_100_0
        elif op_type == '100_1':
            return Parser_100_1
        elif op_type == '100_2':
            return Parser_100_2
        elif op_type == '101_0':
            return Parser_101_0
        elif op_type == '101_1':
            return Parser_101_1
        elif op_type == '101_2':
            return Parser_101_2
        elif op_type == '101_3':
            return Parser_101_3
        elif op_type == '101_4':
            return Parser_101_4
        elif op_type == '110_0':
            return Parser_110_0
        elif op_type == '110_1':
            return Parser_110_1
        elif op_type == '110_2':
            return Parser_110_2
        elif op_type == '111_0':
            return Parser_111_0
        elif op_type == '111_1':
            return Parser_111_1


class BaseParser(object):
    def __init__(self, code_line, tag_pc_dict, data_offset_dict):
        """
        :type code_line: CodeLine
        :type tag_pc_dict: dict
        :type data_offset_dict: dict
        """
        self.code_line = code_line
        self.tag_pc_dict = tag_pc_dict
        self.data_offset_dict = data_offset_dict
        self.imm = bool(int(opcode_encode_dict[code_line.opcode]['imm']))
        self.fraction = None

    def parse_opcode(self):
        if self.code_line.opcode in opcode_encode_dict:
            meta = opcode_encode_dict[self.code_line.opcode]
            return meta['function'] + meta['imm'] + meta['group']
        else:
            print("'{}' is not a valid opcode".format(self.code_line.opcode))
            raise AsmException('opcode parse error')

    def parse_operand(self):
        ret = None
        encode_list = self._operand_encode()
        if None in encode_list:
            none_index = encode_list.index(None)
            print("can not parse operand: {0}".format(
                self.code_line.operand[none_index]))
            raise AsmException("operand parse error")
        else:
            ret = self._set_operand(encode_list)
        return ret

    def _operand_encode(self):
        raise NotImplementedError

    def _set_operand(self, encode_list):
        raise NotImplementedError

    def preprocess(self):
        pass

    def parse_code(self):
        ret = ['0'] * 64
        self.preprocess()
        ret[-12:] = self.parse_opcode()
        ret[2:-12] = self.parse_operand()
        return ret


class Parser_000_0(BaseParser):
    def _operand_encode(self):
        encode0 = None
        encode1 = None
        encode2 = None
        if len(self.code_line.operand) >= 3:
            encode0 = parse_reg(self.code_line.operand[0], ['sr'])
            encode1 = parse_reg(self.code_line.operand[1], ['sr'])
            encode2 = parse_j_imm(self.code_line.operand[2], self.code_line.pc,
                                  self.tag_pc_dict)
        return [encode0, encode1, encode2]

    def _set_operand(self, encode_list):
        ret = ['0'] * OPERAND_ENCODE_WIDTH
        set_d(ret, encode_list[0])
        set_a(ret, encode_list[1])
        set_imm(ret, encode_list[2])
        return ret


class Parser_000_1(BaseParser):
    def _operand_encode(self):
        encode0 = None
        encode1 = None
        encode2 = None
        if len(self.code_line.operand) >= 3:
            encode0 = parse_reg(self.code_line.operand[0], ['sr'])
            encode1 = parse_reg(self.code_line.operand[1], ['sr'])
            encode2 = parse_j_imm(self.code_line.operand[2],
                                  self.code_line.pc,
                                  self.tag_pc_dict)
        return [encode0, encode1, encode2]

    def _set_operand(self, encode_list):
        ret = ['0'] * OPERAND_ENCODE_WIDTH
        set_d(ret, encode_list[0])
        set_a(ret, encode_list[1])
        set_imm(ret, encode_list[2])
        return ret


class Parser_000_2(BaseParser):
    def _operand_encode(self):
        return [0]

    def _set_operand(self, encode_list):
        ret = ['0'] * OPERAND_ENCODE_WIDTH
        return ret


class Parser_000_3(BaseParser):
    def _operand_encode(self):
        encode0 = None
        encode1 = None
        encode2 = None
        if len(self.code_line.operand) >= 3:
            encode0 = parse_reg(self.code_line.operand[0], ['sr'])
            encode1 = parse_reg(self.code_line.operand[1], ['sr'])
            encode2 = parse_reg_imm(self.imm,
                                    self.data_offset_dict,
                                    self.code_line.operand[2], ['sr'])
        return [encode0, encode1, encode2]

    def _set_operand(self, encode_list):
        ret = ['0'] * OPERAND_ENCODE_WIDTH
        set_d(ret, encode_list[0])
        set_a(ret,  encode_list[0])
        set_b_imm(self.imm, ret,  encode_list[0])
        return ret

    def preprocess(self):
        if check_mem_data_name(self.code_line.operand[2]):
            self.imm = True



class Parser_000_4(BaseParser):
    def _operand_encode(self):
        encode0 = None
        encode1 = None
        if len(self.code_line.operand) >= 2:
            encode0 = parse_reg(self.code_line.operand[0], ['sr'])
            encode1 = parse_imm(self.code_line.operand[1],
                                self.data_offset_dict)
        return [encode0, encode1]

    def _set_operand(self, encode_list):
        ret = ['0'] * OPERAND_ENCODE_WIDTH
        set_d(ret, encode_list[0])
        set_imm(ret, encode_list[1])
        return ret


class Parser_001_0(BaseParser):
    def _operand_encode(self):
        encode0 = None
        encode1 = None
        if len(self.code_line.operand) >= 2:
            encode0 = parse_aux_reg(self.code_line.operand[0])
            encode1 = parse_reg_imm(self.imm,
                                    self.data_offset_dict,
                                    self.code_line.operand[1], ['sr'])
        return [encode0, encode1]

    def _set_operand(self, encode_list):
        ret = ['0'] * OPERAND_ENCODE_WIDTH
        set_d(ret, encode_list[0])
        set_a_imm(self.imm, ret, encode_list[1])
        return ret


class Parser_001_1(BaseParser):
    def _operand_encode(self):
        encode0 = None
        encode1 = None
        if len(self.code_line.operand) >= 2:
            encode0 = parse_reg(self.code_line.operand[0], ['sr'])
            encode1 = parse_aux_reg(self.code_line.operand[1])
        return [encode0, encode1]

    def _set_operand(self, encode_list):
        ret = ['0'] * OPERAND_ENCODE_WIDTH
        set_d(ret, encode_list[0])
        set_imm(ret, encode_list[1])
        return ret


class Parser_010_0(BaseParser):
    def _operand_encode(self):
        encode0 = None
        encode1 = None
        encode2 = None
        if len(self.code_line.operand) >= 3:
            encode0 = parse_reg(self.code_line.operand[0], ['vr', 'vs', 'pr'])
            encode1 = parse_reg(self.code_line.operand[1], ['sr'])
            encode2 = parse_reg_imm(self.imm,
                                    self.data_offset_dict,
                                    self.code_line.operand[2], ['sr'])
        return [encode0, encode1, encode2]

    def _set_operand(self, encode_list):
        ret = ['0'] * OPERAND_ENCODE_WIDTH
        set_d(ret, encode_list[0])
        set_a(ret, encode_list[1])
        set_b_imm(self.imm, ret, encode_list[2])
        return ret

    def preprocess(self):
        if check_mem_data_name(self.code_line.operand[2]):
            self.imm = True



class Parser_011_0(BaseParser):
    def _operand_encode(self):
        encode0 = None
        encode1 = None
        encode2 = None
        if len(self.code_line.operand) >= 3:
            encode0 = parse_reg(self.code_line.operand[0], ['vr'])
            encode1 = parse_reg(self.code_line.operand[1], ['sr'])
            encode2 = parse_reg(self.code_line.operand[2], ['sr'])
        return [encode0, encode1, encode2]

    def _set_operand(self, encode_list):
        ret = ['0'] * OPERAND_ENCODE_WIDTH
        set_d(ret, encode_list[0])
        set_a(ret, encode_list[0])
        set_b(ret, encode_list[0])
        return ret


class Parser_100_0(BaseParser):
    def _operand_encode(self):
        encode0 = None
        encode1 = None
        if len(self.code_line.operand) >= 2:
            a_encode_list = ['vr', 'vs', 'sr']
            if self.code_line.operand[0] == 'pr':
                a_encode_list.remove('vs')
            encode0 = parse_reg(self.code_line.operand[0], ['vr', 'vs', 'pr'])
            encode1 = parse_reg_imm(self.imm,
                                    self.data_offset_dict,
                                    self.code_line.operand[1],
                                    a_encode_list)
        return [encode0, encode1]

    def _set_operand(self, encode_list):
        ret = ['0'] * OPERAND_ENCODE_WIDTH
        set_d(ret, encode_list[0])
        set_a_imm(self.imm, ret, encode_list[1])
        return ret


class Parser_100_1(BaseParser):
    def _operand_encode(self):
        encode0 = None
        encode1 = None
        if len(self.code_line.operand) >= 2:
            encode0 = parse_reg(self.code_line.operand[0], ['vr', 'pr'])
            encode1 = parse_reg(self.code_line.operand[1], ['vr', 'vs'])
        return [encode0, encode1]

    def _set_operand(self, encode_list):
        ret = ['0'] * OPERAND_ENCODE_WIDTH
        set_d(ret, encode_list[0])
        set_a(ret, encode_list[1])
        return ret


class Parser_100_2(BaseParser):
    def _operand_encode(self):
        encode0 = None
        encode1 = None
        if len(self.code_line.operand) >= 2:
            encode0 = parse_reg(self.code_line.operand[0], ['vr', 'vs'])
            encode1 = parse_reg(self.code_line.operand[1], ['vr', 'pr'])
        return [encode0, encode1]

    def _set_operand(self, encode_list):
        ret = ['0'] * OPERAND_ENCODE_WIDTH
        set_d(ret, encode_list[0])
        set_a(ret, encode_list[1])
        return ret


class Parser_101_0(BaseParser):
    def _operand_encode(self):
        encode0 = None
        encode1 = None
        encode2 = None
        if len(self.code_line.operand) >= 3:
            encode0 = parse_reg(self.code_line.operand[0], ['vr'])
            encode1 = parse_reg(self.code_line.operand[1], ['vr'])
            encode2 = parse_reg_imm(self.imm,
                                    self.data_offset_dict,
                                    self.code_line.operand[2],
                                    ['vr', 'sr'])
        return [encode0, encode1, encode2]

    def _set_operand(self, encode_list):
        ret = ['0'] * OPERAND_ENCODE_WIDTH
        set_d(ret, encode_list[0])
        set_a(ret, encode_list[1])
        set_b_imm(self.imm, ret, encode_list[2])
        return ret

    def preprocess(self):
        if self.imm and check_num(self.code_line.operand[2]):
            if len(self.code_line.operand) >= 4:
                self.fraction = \
                    int(self.code_line.operand[3].split('=')[-1].strip())

            if self.code_line.dtype == 'f':
                self.code_line.operand[2] = '0b' + \
                    single2bin(self.code_line.operand[2])
            elif self.code_line.dtype == 'w':
                self.code_line.operand[2] = '0b' + \
                    fix322bin(self.code_line.operand[2], self.fraction)
            elif self.code_line.dtype == 'h':
                self.code_line.operand[2] = '0b' + \
                    fix162bin(self.code_line.operand[2], self.fraction)
            elif self.code_line.dtype == 'b':
                self.code_line.operand[2] = '0b' + \
                    fix82bin(self.code_line.operand[2], self.fraction)
            elif self.code_line.dtype == 'hb':
                self.code_line.operand[2] = '0b' + \
                    fix42bin(self.code_line.operand[2], self.fraction)


class Parser_101_1(BaseParser):
    def _operand_encode(self):
        encode0 = None
        encode1 = None
        if len(self.code_line.operand) >= 2:
            encode0 = parse_reg(self.code_line.operand[0], ['vr', 'pr'])
            encode1 = parse_reg(self.code_line.operand[1], ['vr'])
        return [encode0, encode1]

    def _set_operand(self, encode_list):
        ret = ['0'] * OPERAND_ENCODE_WIDTH
        set_d(ret, encode_list[0])
        set_a(ret, encode_list[1])
        return ret


class Parser_101_2(BaseParser):
    def _operand_encode(self):
        encode0 = None
        encode1 = None
        encode2 = None
        if len(self.code_line.operand) >= 3:
            encode0 = parse_reg(self.code_line.operand[0], ['vr'])
            encode1 = parse_reg(self.code_line.operand[1], ['vr'])
            encode2 = parse_reg_imm(self.imm,
                                    self.data_offset_dict,
                                    self.code_line.operand[2],
                                    ['sr'])
        return [encode0, encode1, encode2]

    def _set_operand(self, encode_list):
        ret = ['0'] * OPERAND_ENCODE_WIDTH
        set_d(ret, encode_list[0])
        set_a(ret, encode_list[1])
        set_b_imm(self.imm, ret, encode_list[2])
        return ret


class Parser_101_3(BaseParser):
    def _operand_encode(self):
        encode0 = None
        encode1 = None
        encode2 = None
        if len(self.code_line.operand) >= 3:
            encode0 = parse_reg(self.code_line.operand[0], ['vr', 'pr'])
            encode1 = parse_reg(self.code_line.operand[1], ['vr'])
            encode2 = parse_reg(self.code_line.operand[2], ['vr', 'vs'])
        return [encode0, encode1, encode2]

    def _set_operand(self, encode_list):
        ret = ['0'] * OPERAND_ENCODE_WIDTH
        set_d(ret, encode_list[0])
        set_a(ret, encode_list[1])
        set_b(ret, encode_list[2])
        return ret


class Parser_101_4(BaseParser):
    def _operand_encode(self):
        encode0 = None
        encode1 = None
        if len(self.code_line.operand) >= 2:
            encode0 = parse_reg(self.code_line.operand[0], ['vr'])
            encode1 = parse_reg(self.code_line.operand[1], ['vr'])
        return [encode0, encode1]

    def _set_operand(self, encode_list):
        ret = ['0'] * OPERAND_ENCODE_WIDTH
        set_d(ret, encode_list[0])
        set_a(ret, encode_list[1])
        return ret


class Parser_110_0(BaseParser):
    def _operand_encode(self):
        encode0 = None
        encode1 = None
        encode2 = None
        if len(self.code_line.operand) >= 3:
            encode0 = parse_reg(self.code_line.operand[0], ['vr'])
            encode1 = parse_reg(self.code_line.operand[1], ['vr'])
            encode2 = parse_reg(self.code_line.operand[2], ['vr', 'vs'])
        return [encode0, encode1, encode2]

    def _set_operand(self, encode_list):
        ret = ['0'] * OPERAND_ENCODE_WIDTH
        set_d(ret, encode_list[0])
        set_a(ret, encode_list[1])
        set_b(ret, encode_list[2])
        return ret


class Parser_110_1(BaseParser):
    def _operand_encode(self):
        encode0 = None
        encode1 = None
        encode2 = None
        if len(self.code_line.operand) >= 3:
            encode0 = parse_reg(self.code_line.operand[0], ['vr'])
            encode1 = parse_reg(self.code_line.operand[1], ['vr'])
            encode2 = parse_reg(self.code_line.operand[2], ['vs'])
        return [encode0, encode1, encode2]

    def _set_operand(self, encode_list):
        ret = ['0'] * OPERAND_ENCODE_WIDTH
        set_d(ret, encode_list[0])
        set_a(ret, encode_list[1])
        set_b(ret, encode_list[2])
        return ret


class Parser_110_2(BaseParser):
    def _operand_encode(self):
        encode0 = None
        encode1 = None
        if len(self.code_line.operand) >= 2:
            encode0 = parse_reg(self.code_line.operand[0], ['vr'])
            encode1 = parse_reg(self.code_line.operand[1], ['vr'])
        return [encode0, encode1]

    def _set_operand(self, encode_list):
        ret = ['0'] * OPERAND_ENCODE_WIDTH
        set_d(ret, encode_list[0])
        set_a(ret, encode_list[1])
        return ret


class Parser_111_0(BaseParser):
    def _operand_encode(self):
        encode0 = None
        encode1 = None
        encode2 = None
        if len(self.code_line.operand) >= 3:
            encode0 = parse_reg(self.code_line.operand[0], ['vr'])
            encode1 = parse_reg(self.code_line.operand[1], ['vr'])
            encode2 = parse_reg_imm(self.imm,
                                    self.data_offset_dict,
                                    self.code_line.operand[2],
                                    ['vr', 'sr'])
        return [encode0, encode1, encode2]

    def _set_operand(self, encode_list):
        ret = ['0'] * OPERAND_ENCODE_WIDTH
        set_d(ret, encode_list[0])
        set_a(ret, encode_list[1])
        set_b_imm(self.imm, ret, encode_list[1])
        return ret


class Parser_111_1(BaseParser):
    def _operand_encode(self):
        encode0 = None
        encode1 = None
        encode2 = None
        if len(self.code_line.operand) >= 3:
            encode0 = parse_reg(self.code_line.operand[0], ['vr'])
            encode1 = parse_reg(self.code_line.operand[1], ['vr'])
            encode2 = parse_reg_imm(self.imm,
                                    self.data_offset_dict,
                                    self.code_line.operand[2],
                                    ['sr'])
        return [encode0, encode1, encode2]

    def _set_operand(self, encode_list):
        ret = ['0'] * OPERAND_ENCODE_WIDTH
        set_d(ret, encode_list[0])
        set_a(ret, encode_list[1])
        set_b_imm(self.imm, ret, encode_list[2])
        return ret

