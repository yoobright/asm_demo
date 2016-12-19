# -*- coding: utf-8 -*-
from exception_util import AsmException


def get_imm_opcode(input_str):
    if input_str == 'i':
        return '1'
    return '0'


def get_bit_width_opcode(input_str):
    if input_str == 'f':
        return '000'
    elif input_str == 'hb':
        return '001'
    elif input_str == 'b':
        return '010'
    elif input_str == 'h':
        return '011'
    elif input_str == 'w':
        return '100'
    else:
        raise AsmException('not a valid bit width')


# reg
# ==============================================================================
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

# aux reg
# ==============================================================================
aux_reg_encode_dict = {
    'aux_identity': 0x0,
    'aux_fetchpc': 0x4,
    'aux_pause': 0x5,
    'aux_run': 0x6,
    'aux_stop': 0x7,
    'aux_psw': 0x8,
    'aux_vlen0': 0x20,
    'aux_updw': 0x23,
    'aux_vlen1': 0x21,
    'aux_vlen2': 0x22,
    'aux_sldstrd1': 0x24,
    'aux_sldstrd2': 0x25,
    'aux_actln': 0x28,
    'aux_actpe': 0x29,
    'aux_lsvlen': 0x30,
    'aux_lsvln': 0x31,
    'aux_lsvhv': 0x32,
    'aux_lsvridx': 0x33,
    'aux_lsvcidx': 0x34,
    'aux_lsvstrd': 0x35,
    'aux_lsvrow': 0x37,
    'aux_lsvrowstrd': 0x38,
    'aux_lsvpad': 0x26,
    'aux_ilvlnsrc': 0x40,
    'aux_ilvpesrc': 0x41,
    'aux_ilvlndst': 0x42,
    'aux_ilvpedst': 0x43,
    'aux_ilvlen': 0x44,
    'aux_ilvpad': 0x45,
    'aux_fprnd': 0x50,
    'aux_intrnd': 0x54,
    'aux_intsat': 0x55,
    'aux_intfxdp': 0x56
}

# opcode
# ==============================================================================

# group 000
opcode_encode_dict = {
    's_jal': {'function': '00000000', 'imm': '0', 'group': '000'},
    's_jalr': {'function': '00000000', 'imm': '0', 'group': '000'},
    's_beq': {'function': '00000000', 'imm': '0', 'group': '000'},
    's_bne': {'function': '00000000', 'imm': '0', 'group': '000'},
    's_bge': {'function': '00000000', 'imm': '0', 'group': '000'},
    's_bltu': {'function': '00000000', 'imm': '0', 'group': '000'},
    's_bgeu': {'function': '00000000', 'imm': '0', 'group': '000'},
    's_wauxi': {'function': '00000000', 'imm': '0', 'group': '000'},
    's_rauxi': {'function': '00000000', 'imm': '0', 'group': '000'},
    's_sync': {'function': '00000000', 'imm': '0', 'group': '000'},
    's_movi': {'function': '00000000', 'imm': '0', 'group': '000'},
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
    print('=' * 20)
    print(aux_reg_encode_dict)
    print('=' * 20)
    print(opcode_encode_dict)
