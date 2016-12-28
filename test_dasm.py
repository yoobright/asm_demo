# -*- coding: utf-8 -*-

import subprocess
import os


def get_coe_file(dir_name):
    file_list = []
    for asm_file in os.listdir(dir_name):
        if asm_file.endswith(".coe"):
            asm_file_name = os.path.join(dir_name, asm_file)
            file_list.append(asm_file_name)
    return file_list

cmd_temp = "python disassemble.py -i {0} -v"
file_name = "test\\dtest.txt"
cmd_str = cmd_temp.format(file_name)
subprocess.call(cmd_str, shell=True)
