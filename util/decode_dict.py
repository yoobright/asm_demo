# -*- coding: utf-8 -*-
from __future__ import print_function
from encode_dict import reg_encode_dict

reg_decode_dict = {}
for key, value in reg_encode_dict.items():
    reg_decode_dict[value] = key


if __name__ == '__main__':
    print(reg_decode_dict)
