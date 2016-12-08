# -*- coding: utf-8 -*-
from __future__ import print_function
from exception_util import *
from encode_dict import opcode_encode_dict
import re
import pprint

state = None

data_line_list = []
code_line_list = []
tag_pc_dict = {}
data_offset_dict = {}

# data_list = []

pc_count = 0
line_count = 1
addr_offset = 0
type_list = ['word']


def get_data_elem(line):
    pattern = re.compile(r'\s+|,\s*')
    data_name, data_type, data_size = pattern.split(line.strip())

    if data_type not in type_list:
        print("'{0}' is not a valid data type".format(data_type))
        raise AsmException("data type check error")
    if not data_size.isdigit():
        print("'{0}' is not a valid data size".format(data_size))
        raise AsmException("data size check error")

    if data_type == 'word':
        data_size = int(data_size) * 4
    else:
        data_size = int(data_size)

    return data_name, data_type, data_size


def get_code_elem(line):
    pattern = re.compile(r'\s+|,\s*')
    split_line = pattern.split(line.strip())
    opcode = split_line[0]
    operand = split_line[1:]
    if opcode not in opcode_encode_dict:
        print("'{0}' is not a valid opcode".format(opcode))
        raise AsmException('opcode check error')
    return opcode, operand


class DataLine:
    def __init__(self, line, addr_offset=addr_offset):
        self.line = line
        self.data_name, self.data_type, self.data_size = get_data_elem(
            self.line)
        self.addr_offset = addr_offset

    def __repr__(self):
        return 'name: {0}, type: {1}, size: {2}, addr_offset: {3}'.format(
            self.data_name, self.data_type, self.data_size, self.addr_offset)


class CodeLine:
    def __init__(self, line, pc):
        self.line = line
        self.pc = pc
        self.opcode, self.operand = get_code_elem(line)
        self.encode_list = None

    def __repr__(self):
        return 'opcode: {0}, operand: {1} pc: {2}'.format(
            self.opcode, self.operand, self.pc)

    def get_encode(self):
        if self.encode_list:
            return ''.join(self.encode_list)


with open("test.txt") as f:
    for file_line in f.readlines():
        try:
            line_data = file_line.strip().split('#')[0].strip().lower()
            if line_data.startswith('_data'):
                state = 'data'
                line_count += 1
                continue
            if line_data.startswith('_code'):
                state = 'code'
                line_count += 1
                continue

            if state == 'data' and line_data:
                data_line = DataLine(line_data, addr_offset)
                data_line_list.append(data_line)
                addr_offset += data_line.data_size
                data_offset_dict[data_line.data_name] = data_line.addr_offset

            if state == 'code' and line_data:
                if ':' in line_data:
                    tag, line_data, = line_data.split(':')
                    tag_pc_dict[tag] = pc_count
                code_line_list.append(CodeLine(line_data, pc_count))
                pc_count += 1
            line_count += 1
        except AsmException as ex:
            print("Asm exception in line: {0}".format(line_count))
            raise ex


pp = pprint.PrettyPrinter(indent=4)
print("=====data_line_list=====")
pp.pprint(data_line_list)
print("=====code_line_list=====")
pp.pprint(code_line_list)
print("=====data_offset_dict=====")
pp.pprint(data_offset_dict)
print("=====tag_pc_dict=====")
pp.pprint(tag_pc_dict)


for code_line in code_line_list:
    print(code_line.get_encode())