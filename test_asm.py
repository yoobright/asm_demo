# -*- coding: utf-8 -*-
import subprocess

cmd_temp = "python assemble.py -i {0} -v"
file_name = "test.txt"
cmd_str = cmd_temp.format(file_name)
subprocess.call(cmd_str, shell=True)
