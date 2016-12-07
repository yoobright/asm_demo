# -*- coding: utf-8 -*-

reg_encode_dict = {}

# add sr
for i in range(32):
    key = 'sr{0}'.format(i)
    reg_encode_dict[key] = "{:0>5b}".format(i)

# add vr
for i in range(8):
    key = 'vr{0}'.format(i)
    reg_encode_dict[key] = "{:0>5b}".format(i)

# add vs
for i in range(3):
    key = 'vs{0}'.format(i)
    reg_encode_dict[key] = "{:0>5b}".format(i + 16)

# add pr
reg_encode_dict['pr'] = '111111'


opcode_encode_dict = {
    's_jal': ['0010000'],
    's_jalr': ['0000000'],
    's_beq': [''],
    's_bne': [''],
    's_bge': [''],
    's_bltu': [''],
    's_bgeu': [''],
    's_wauxi': [''],
    's_rauxi': [''],
    's_sync': [''],
    's_movi': [''],
}

for i in ['', 'i']:
    opcode_encode_dict['s_add' + i] = ['']
    opcode_encode_dict['s_sub' + i] = ['']
    opcode_encode_dict['s_and' + i] = ['']
    opcode_encode_dict['s_or' + i] = ['']
    opcode_encode_dict['s_xor' + i] = ['']
    opcode_encode_dict['s_sll' + i] = ['']
    opcode_encode_dict['s_srl' + i] = ['']
    opcode_encode_dict['s_sra' + i] = ['']
    opcode_encode_dict['s_mulw' + i] = ['']

for i in ['_b', '_h', '_w']:
    opcode_encode_dict['v_ld' + i] = ['']
    opcode_encode_dict['v_st' + i] = ['']
    opcode_encode_dict['v_ilmov' + i] = ['']
    opcode_encode_dict['v_ilbrcst' + i] = ['']


for i in ['', 'i']:
    for j in ['_f', '_hb', '_b', '_h', '_w']:
        opcode_encode_dict['v_mov' + i + j] = ['']
        opcode_encode_dict['v_add' + i + j] = ['']
        opcode_encode_dict['v_sub' + i + j] = ['']
        opcode_encode_dict['v_dotmul' + i + j] = ['']
        opcode_encode_dict['v_xor' + i + j] = ['']
        opcode_encode_dict['v_or' + i + j] = ['']
        opcode_encode_dict['v_and' + i + j] = ['']
        opcode_encode_dict['v_not' + i + j] = ['']

for i in ['', 'i']:
    for j in ['_hb', 'b', 'h', 'w']:
        opcode_encode_dict['v_shl' + i + j] = ['']
        opcode_encode_dict['v_shr' + i + j] = ['']
        opcode_encode_dict['v_shar' + i + j] = ['']
        opcode_encode_dict['v_rol' + i + j] = ['']
        opcode_encode_dict['v_ror' + i + j] = ['']
        opcode_encode_dict['v_fi2fi' + i + j] = ['']


for i in ['_f', '_hb', '_b', '_h', '_w']:
    opcode_encode_dict['v_sum' + i] = ['']
    opcode_encode_dict['v_relu' + i] = ['']
    opcode_encode_dict['v_mul' + i] = ['']
    opcode_encode_dict['v_sigmoid' + i] = ['']
    opcode_encode_dict['v_tanh' + i] = ['']
    opcode_encode_dict['v_exp' + i] = ['']
    opcode_encode_dict['v_log' + i] = ['']
    opcode_encode_dict['v_div' + i] = ['']
    opcode_encode_dict['v_cnv1d' + i] = ['']
    opcode_encode_dict['v_cnv2d' + i] = ['']
    opcode_encode_dict['v_maxpolling1d' + i] = ['']
    opcode_encode_dict['v_maxpolling2d' + i] = ['']


if __name__ == '__main__':
    print(reg_encode_dict)
    print(opcode_encode_dict)
