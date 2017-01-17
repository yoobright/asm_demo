# -*- coding: utf-8 -*-
import subprocess
import os


def get_asm_file(dir_name):
    file_list = []
    for asm_file in os.listdir(dir_name):
        if asm_file.endswith(".asm"):
            asm_file_name = os.path.join(dir_name, asm_file)
            file_list.append(asm_file_name)
    return file_list

cmd_temp = "python assemble.py -i {0} -v -o test\\dtest.txt"
file_name = "test\\test.txt"
cmd_str = cmd_temp.format(file_name)
subprocess.call(cmd_str, shell=True)

# print(get_asm_file("test\\lenet_fixed8"))
