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


op_code_encode_dict = {
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
    op_code_encode_dict['s_add' + i] = ['']
    op_code_encode_dict['s_sub' + i] = ['']
    op_code_encode_dict['s_and' + i] = ['']
    op_code_encode_dict['s_or' + i] = ['']
    op_code_encode_dict['s_xor' + i] = ['']
    op_code_encode_dict['s_sll' + i] = ['']
    op_code_encode_dict['s_srl' + i] = ['']
    op_code_encode_dict['s_sra' + i] = ['']
    op_code_encode_dict['s_mulw' + i] = ['']

for i in ['_b', '_h', '_w']:
    op_code_encode_dict['v_ld' + i] = ['']
    op_code_encode_dict['v_st' + i] = ['']
    op_code_encode_dict['v_ilmov' + i] = ['']
    op_code_encode_dict['v_ilbrcst' + i] = ['']


for i in ['', 'i']:
    for j in ['_f', '_hb', '_b', '_h', '_w']:
        op_code_encode_dict['v_mov' + i + j] = ['']
        op_code_encode_dict['v_add' + i + j] = ['']
        op_code_encode_dict['v_sub' + i + j] = ['']
        op_code_encode_dict['v_dotmul' + i + j] = ['']
        op_code_encode_dict['v_xor' + i + j] = ['']
        op_code_encode_dict['v_or' + i + j] = ['']
        op_code_encode_dict['v_and' + i + j] = ['']
        op_code_encode_dict['v_not' + i + j] = ['']

for i in ['', 'i']:
    for j in ['_hb', 'b', 'h', 'w']:
        op_code_encode_dict['v_shl' + i + j] = ['']
        op_code_encode_dict['v_shr' + i + j] = ['']
        op_code_encode_dict['v_shar' + i + j] = ['']
        op_code_encode_dict['v_rol' + i + j] = ['']
        op_code_encode_dict['v_ror' + i + j] = ['']
        op_code_encode_dict['v_fi2fi' + i + j] = ['']


for i in ['_f', '_hb', '_b', '_h', '_w']:
    op_code_encode_dict['v_sum' + i] = ['']
    op_code_encode_dict['v_relu' + i] = ['']
    op_code_encode_dict['v_mul' + i] = ['']
    op_code_encode_dict['v_sigmoid' + i] = ['']
    op_code_encode_dict['v_tanh' + i] = ['']
    op_code_encode_dict['v_exp' + i] = ['']
    op_code_encode_dict['v_log' + i] = ['']
    op_code_encode_dict['v_div' + i] = ['']
    op_code_encode_dict['v_cnv1d' + i] = ['']
    op_code_encode_dict['v_cnv2d' + i] = ['']
    op_code_encode_dict['v_maxpolling1d' + i] = ['']
    op_code_encode_dict['v_maxpolling2d' + i] = ['']


if __name__ == '__main__':
    print(reg_encode_dict)
    print(op_code_encode_dict)
