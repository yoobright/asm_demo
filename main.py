# -*- coding: utf-8 -*-
from __future__ import print_function
import re

state = None

data_line_list = []
code_line_list = []

# data_list = []

pc_count = 0
addr_offset = 0
type_list = ['word']


def get_data_elem(line):
    pattern = re.compile(r'\s+|,\s*')
    data_name, data_type, data_size = pattern.split(line.strip())

    if data_type not in type_list:
        raise Exception("data type check error")
    if not data_size.isdigit():
        raise Exception("data size check error")
    return data_name, data_type, data_size


class DataLine:
    def __init__(self, line, addr_offset=addr_offset):
        self.line = line
        self.data_name, self.data_type, self.data_size = get_data_elem(self.line)
        self.addr_offset = addr_offset

    def __repr__(self):
        return 'line: {}, offset: {}'.format(self.line, self.addr_offset)


class CodeLine:
    def __init__(self, line, pc):
        self.line = line
        self.pc = pc
        self.code_list = [0] * 32

    def __repr__(self):
        return 'line: {}, pc: {}'.format(self.line, self.pc)


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
            print(addr_offset)

        if state == 'code' and line_data:
            code_line_list.append(CodeLine(line_data, pc_count))
            pc_count += 1

print(data_line_list)
print(code_line_list)
