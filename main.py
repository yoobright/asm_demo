# -*- coding: utf-8 -*-
from __future__ import print_function
import re
import pprint

state = None

data_line_list = []
code_line_list = []
tag_dict = {}

# data_list = []

pc_count = 0
addr_offset = 0
type_list = ['word']


def get_data_elem(line):
    pattern = re.compile(r'\s+|,\s*')
    data_name, data_type, data_size = pattern.split(line.strip())

    if data_type not in type_list:
        raise AsmException("data type check error")
    if not data_size.isdigit():
        raise AsmException("data size check error")

    return data_name, data_type, data_size


def get_code_elem(line):
    pattern = re.compile(r'\s+|,\s*')
    splited_line = pattern.split(line.strip())
    op_code = splited_line[0]
    op_num = splited_line[1:]

    return op_code, op_num


class AsmException(Exception):
    def __init__(self, message):
        self.message = message
        super(AsmException, self).__init__(message)


class DataLine:
    def __init__(self, line, addr_offset=addr_offset):
        self.line = line
        self.data_name, self.data_type, self.data_size = get_data_elem(
            self.line)
        self.addr_offset = addr_offset

    def __repr__(self):
        return 'name: {}, type: {}, size: {}, offset: {}'.format(
            self.data_name, self.data_type, self.data_size, self.addr_offset)


class CodeLine:
    def __init__(self, line, pc):
        self.line = line
        self.pc = pc
        self.op_code, self.op_num = get_code_elem(line)
        self.code_list = [0] * 32

    def __repr__(self):
        return 'op_code: {}, op_num: {} pc: {}'.format(
            self.op_code, self.op_num, self.pc)


with open("test.txt") as f:
    for file_line in f.readlines():
        line_data = file_line.strip().split('#')[0].strip().lower()
        if line_data.startswith('_data'):
            state = 'data'
            continue
        if line_data.startswith('_code'):
            state = 'code'
            continue

        if state == 'data' and line_data:
            data_line_list.append(DataLine(line_data, addr_offset))
            addr_offset += int(data_line_list[-1].data_size)

        if state == 'code' and line_data:
            if ':' in line_data:
                tag, line_data, = line_data.split(':')
                tag_dict[tag] = pc_count
            code_line_list.append(CodeLine(line_data, pc_count))
            pc_count += 1

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(data_line_list)
pp.pprint(code_line_list)
pp.pprint(tag_dict)
