# -*- coding: utf-8 -*-
from __future__ import print_function

state = None
data_line_list = []
code_line_list = []
pc_count = 0


class DataLine:
    def __init__(self, line):
        self.line = line

    def __repr__(self):
        return 'line: {}'.format(self.line)


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
            data_line_list.append(DataLine(line_data))

        if state == 'code' and line_data:
            code_line_list.append(CodeLine(line_data, pc_count))
            pc_count += 1

print(data_line_list)
print(code_line_list)
