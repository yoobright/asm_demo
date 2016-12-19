# -*- coding: utf-8 -*-
from exception_util import AsmException
from encode_util import int2bin


def set_imm_opcode(input_str):
    if input_str == 'i':
        return '1'
    return '0'


def set_bit_width_opcode(input_str):
    if input_str == '_f':
        return '000'
    elif input_str == '_hb':
        return '001'
    elif input_str == '_b':
        return '010'
    elif input_str == '_h':
        return '011'
    elif input_str == '_w':
        return '100'
    else:
        raise AsmException('not a valid bit width')


def set_func_opcode(num, bw=None):
    if bw:
        return int2bin(num, 5) + set_bit_width_opcode(bw)
    else:
        return int2bin(num, 8)


def set_meta(function, imm, group):
    return {
        'function': function,
        'imm': imm,
        'group': group}

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
group = '000'
opcode_encode_dict = {
    's_jal': set_meta(set_func_opcode(0), '0', group),
    's_jalr': set_meta(set_func_opcode(1), '0', group),
    's_beq': set_meta(set_func_opcode(2), '0', group),
    's_bne': set_meta(set_func_opcode(3), '0', group),
    's_blt': set_meta(set_func_opcode(4), '0', group),
    's_bltu': set_meta(set_func_opcode(5), '0', group),
    's_bge': set_meta(set_func_opcode(6), '0', group),
    's_bgeu': set_meta(set_func_opcode(7), '0', group),
    's_sync': set_meta(set_func_opcode(8), '0', group),
    's_ld_b': set_meta(set_func_opcode(9), '0', group),
    's_ld_h': set_meta(set_func_opcode(10), '0', group),
    's_ld_w': set_meta(set_func_opcode(11), '0', group),
    's_st_b': set_meta(set_func_opcode(12), '0', group),
    's_st_h': set_meta(set_func_opcode(13), '0', group),
    's_st_w': set_meta(set_func_opcode(14), '0', group),
    's_movi': set_meta(set_func_opcode(15), '0', group),
}

for i in ['', 'i']:
    opcode_encode_dict['s_add' + i] = \
        set_meta(set_func_opcode(16), set_imm_opcode(i), group)
    opcode_encode_dict['s_sub' + i] = \
        set_meta(set_func_opcode(17), set_imm_opcode(i), group)
    opcode_encode_dict['s_and' + i] = \
        set_meta(set_func_opcode(18), set_imm_opcode(i), group)
    opcode_encode_dict['s_or' + i] = \
        set_meta(set_func_opcode(19), set_imm_opcode(i), group)
    opcode_encode_dict['s_xor' + i] = \
        set_meta(set_func_opcode(20), set_imm_opcode(i), group)
    opcode_encode_dict['s_sll' + i] = \
        set_meta(set_func_opcode(21), set_imm_opcode(i), group)
    opcode_encode_dict['s_srl' + i] = \
        set_meta(set_func_opcode(22), set_imm_opcode(i), group)
    opcode_encode_dict['s_sra' + i] = \
        set_meta(set_func_opcode(23), set_imm_opcode(i), group)
    opcode_encode_dict['s_mulw' + i] = \
        set_meta(set_func_opcode(24), set_imm_opcode(i), group)
    opcode_encode_dict['s_cmpeq' + i] = \
        set_meta(set_func_opcode(25), set_imm_opcode(i), group)
    opcode_encode_dict['s_cmpne' + i] = \
        set_meta(set_func_opcode(26), set_imm_opcode(i), group)
    opcode_encode_dict['s_cmplt' + i] = \
        set_meta(set_func_opcode(27), set_imm_opcode(i), group)
    opcode_encode_dict['s_cmpltu' + i] = \
        set_meta(set_func_opcode(28), set_imm_opcode(i), group)
    opcode_encode_dict['s_cmpgt' + i] = \
        set_meta(set_func_opcode(29), set_imm_opcode(i), group)
    opcode_encode_dict['s_cmpgtu' + i] = \
        set_meta(set_func_opcode(30), set_imm_opcode(i), group)

opcode_encode_dict['nop'] = set_meta(set_func_opcode(31), '0', group),

# group 001
group = '001'
opcode_encode_dict['s_waux'] = set_meta(set_func_opcode(0), '0', group)
opcode_encode_dict['s_wauxi'] = set_meta(set_func_opcode(0), '1', group)
opcode_encode_dict['s_rauxi'] = set_meta(set_func_opcode(1), '1', group)


# group 010
group = '010'
for i in ['_b', '_h', '_w']:
    opcode_encode_dict['v_ld' + i] = ['']
    opcode_encode_dict['v_st' + i] = ['']


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
    for j in ['_hb', '_b', '_h', '_w']:
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
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(reg_encode_dict)
    print('=' * 20)
    pp.pprint(aux_reg_encode_dict)
    print('=' * 20)
    pp.pprint(opcode_encode_dict)
