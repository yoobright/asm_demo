# -*- coding: utf-8 -*-

from __future__ import print_function
import re
from deModel import DeFixedInt

pattern = re.compile(r'\$\((\w+)\)')

print(list('101'))
print(''.join(['1', '2', '3']))

print('{:b}'.format(-2 & 0xff))

a = DeFixedInt(8, 4, -1)
b = DeFixedInt(8, 4, 1111)
print(a + b)
print(a)
print(hex(a))
print(a.width)
print(a.bit())
