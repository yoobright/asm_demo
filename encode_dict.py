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


def set_meta(function, imm, group, type):
    return {
        'function': function,
        'imm': imm,
        'group': group,
        'type': group + '_' + type}

# reg
# ==============================================================================
# add sr
sr_encode_dict = {}
for i in range(32):
    key = 'sr{0}'.format(i)
    sr_encode_dict[key] = "{:0>6b}".format(i)

# add vr
vr_encode_dict = {}
for i in range(9):
    key = 'vr{0}'.format(i)
    vr_encode_dict[key] = "{:0>6b}".format(i + 32)

# add vs
vs_encode_dict = {}
for i in range(5):
    key = 'vs{0}'.format(i)
    vs_encode_dict[key] = "{:0>6b}".format(i + 48)

# add pr
pr_encode_dict = {'pr': '111111'}

reg_encode_dict = dict(
    sr_encode_dict.items() +
    vr_encode_dict.items() +
    vs_encode_dict.items() +
    pr_encode_dict.items()
    )

# aux reg
# ==============================================================================
aux_reg_encode_dict = {
    # ID
    'aux_identity': 0,
    # flow control
    'aux_fetchpc': 1,
    'aux_pause': 2,
    'aux_run': 3,
    'aux_stop': 4,
    'aux_psw': 5,
    # Vector Move Control
    'aux_mvvrow': 6,
    'aux_mvvsridx': 7,
    'aux_mvvscidx': 8,
    'aux_mvvdridx': 9,
    'aux_mvvdcidx': 10,
    # Vector Computation Control
    'aux_vlen0': 12,
    'aux_updw': 13,
    'aux_vlen1': 14,
    'aux_vlen2': 15,
    'aux_sldstrd1': 16,
    'aux_sldstrd2': 17,
    'aux_actln': 18,
    'aux_actpe': 19,
    # Vector Load/Store Control
    'aux_lsvlen': 20,
    'aux_lsvln': 21,
    'aux_lsvhv': 22,
    'aux_lsvridx': 23,
    'aux_lsvcidx': 24,
    'aux_lsvstrd': 25,
    'aux_lsvrow': 26,
    'aux_lsvrowstrd': 27,
    'aux_lsvpad': 28,
    # Inter-Lane Transfer Control
    'aux_ilvlnsrc': 29,
    'aux_ilvpesrc': 30,
    'aux_ilvlndst': 31,
    'aux_ilvpedst': 32,
    'aux_ilvlen': 33,
    'aux_ilvpad': 34,
    # Arithmetic Mode
    'aux_fprnd': 35,
    'aux_intrnd': 36,
    'aux_intsat': 37,
    'aux_intfxdp': 38
}

# opcode
# ==============================================================================
opcode_encode_dict = {}
# group 000
group = '000'
opcode_encode_dict['s_jal'] = set_meta(set_func_opcode(0), '1', group, '0')
opcode_encode_dict['s_jalr'] = set_meta(set_func_opcode(1), '1', group, '0')
opcode_encode_dict['s_beq'] = set_meta(set_func_opcode(2), '1', group, '1')
opcode_encode_dict['s_bne'] = set_meta(set_func_opcode(3), '1', group, '1')
opcode_encode_dict['s_blt'] = set_meta(set_func_opcode(4), '1', group, '1')
opcode_encode_dict['s_bltu'] = set_meta(set_func_opcode(5), '1', group, '1')
opcode_encode_dict['s_bge'] = set_meta(set_func_opcode(6), '1', group, '1')
opcode_encode_dict['s_bgeu'] = set_meta(set_func_opcode(6), '1', group, '1')
opcode_encode_dict['s_sync'] = set_meta(set_func_opcode(8), '0', group, '2')
opcode_encode_dict['s_ld_b'] = set_meta(set_func_opcode(9), '0', group, '3')
opcode_encode_dict['s_ld_h'] = set_meta(set_func_opcode(10), '0', group, '3')
opcode_encode_dict['s_ld_w'] = set_meta(set_func_opcode(11), '0', group, '3')
opcode_encode_dict['s_st_b'] = set_meta(set_func_opcode(12), '0', group, '3')
opcode_encode_dict['s_st_h'] = set_meta(set_func_opcode(13), '0', group, '3')
opcode_encode_dict['s_st_w'] = set_meta(set_func_opcode(14), '0', group, '3')
opcode_encode_dict['s_movi'] = set_meta(set_func_opcode(15), '1', group, '4')

for i in ['', 'i']:
    opcode_encode_dict['s_add' + i] = \
        set_meta(set_func_opcode(16), set_imm_opcode(i), group, '3')
    opcode_encode_dict['s_sub' + i] = \
        set_meta(set_func_opcode(17), set_imm_opcode(i), group, '3')
    opcode_encode_dict['s_and' + i] = \
        set_meta(set_func_opcode(18), set_imm_opcode(i), group, '3')
    opcode_encode_dict['s_or' + i] = \
        set_meta(set_func_opcode(19), set_imm_opcode(i), group, '3')
    opcode_encode_dict['s_xor' + i] = \
        set_meta(set_func_opcode(20), set_imm_opcode(i), group, '3')
    opcode_encode_dict['s_sll' + i] = \
        set_meta(set_func_opcode(21), set_imm_opcode(i), group, '3')
    opcode_encode_dict['s_srl' + i] = \
        set_meta(set_func_opcode(22), set_imm_opcode(i), group, '3')
    opcode_encode_dict['s_sra' + i] = \
        set_meta(set_func_opcode(23), set_imm_opcode(i), group, '3')
    opcode_encode_dict['s_mulw' + i] = \
        set_meta(set_func_opcode(24), set_imm_opcode(i), group, '3')
    opcode_encode_dict['s_cmpeq' + i] = \
        set_meta(set_func_opcode(25), set_imm_opcode(i), group, '3')
    opcode_encode_dict['s_cmpne' + i] = \
        set_meta(set_func_opcode(26), set_imm_opcode(i), group, '3')
    opcode_encode_dict['s_cmplt' + i] = \
        set_meta(set_func_opcode(27), set_imm_opcode(i), group, '3')
    opcode_encode_dict['s_cmpltu' + i] = \
        set_meta(set_func_opcode(28), set_imm_opcode(i), group, '3')
    opcode_encode_dict['s_cmpgt' + i] = \
        set_meta(set_func_opcode(29), set_imm_opcode(i), group, '3')
    opcode_encode_dict['s_cmpgtu' + i] = \
        set_meta(set_func_opcode(30), set_imm_opcode(i), group, '3')

opcode_encode_dict['nop'] = set_meta(set_func_opcode(31), '0', group, '2')

# group 001
group = '001'
opcode_encode_dict['s_waux'] = set_meta(set_func_opcode(0), '0', group, '0')
opcode_encode_dict['s_wauxi'] = set_meta(set_func_opcode(0), '1', group, '0')
opcode_encode_dict['s_rauxi'] = set_meta(set_func_opcode(1), '1', group, '1')


# group 010
group = '010'
for i in ['_b', '_h', '_w']:
    opcode_encode_dict['v_ld' + i] = \
        set_meta(set_func_opcode(0, i), '0', group, '0')
    opcode_encode_dict['v_st' + i] = \
        set_meta(set_func_opcode(1, i), '0', group, '0')

# group 011
group = '011'
for i in ['_b', '_h', '_w']:
    opcode_encode_dict['v_ilmov' + i] = \
        set_meta(set_func_opcode(0, i), '0', group, '0')
    opcode_encode_dict['v_ilbrcst' + i] = \
        set_meta(set_func_opcode(1, i), '0', group, '0')

# group 100
group = '100'
for i in ['_f', '_hb', '_b', '_h', '_w']:
    opcode_encode_dict['v_mov' + i] = \
        set_meta(set_func_opcode(0, i), '0', group, '0')
    opcode_encode_dict['v_movi' + i] = \
        set_meta(set_func_opcode(0, i), '1', group, '0')
    opcode_encode_dict['v_movrtc' + i] = \
        set_meta(set_func_opcode(1, i), '0', group, '1')
    opcode_encode_dict['v_movctr' + i] = \
        set_meta(set_func_opcode(2, i), '0', group, '2')

# group 101
group = '101'
for i in ['', 'i']:
    for j in ['_f', '_hb', '_b', '_h', '_w']:
        opcode_encode_dict['v_add' + i + j] = \
            set_meta(set_func_opcode(0, j), set_imm_opcode(i), group, '0')
        opcode_encode_dict['v_sub' + i + j] = \
            set_meta(set_func_opcode(1, j), set_imm_opcode(i), group, '0')
        opcode_encode_dict['v_cmpeq' + i + j] = \
            set_meta(set_func_opcode(2, j), set_imm_opcode(i), group, '0')
        opcode_encode_dict['v_cmpne' + i + j] = \
            set_meta(set_func_opcode(3, j), set_imm_opcode(i), group, '0')
        opcode_encode_dict['v_cmplt' + i + j] = \
            set_meta(set_func_opcode(4, j), set_imm_opcode(i), group, '0')
        opcode_encode_dict['v_cmpltu' + i + j] = \
            set_meta(set_func_opcode(5, j), set_imm_opcode(i), group, '0')
        opcode_encode_dict['v_cmpgt' + i + j] = \
            set_meta(set_func_opcode(6, j), set_imm_opcode(i), group, '0')
        opcode_encode_dict['v_cmpgtu' + i + j] = \
            set_meta(set_func_opcode(7, j), set_imm_opcode(i), group, '0')
        opcode_encode_dict['v_dotmul' + i + j] = \
            set_meta(set_func_opcode(8, j), set_imm_opcode(i), group, '0')

for i in ['_f', '_hb', '_b', '_h', '_w']:
    opcode_encode_dict['v_sum' + i] = \
        set_meta(set_func_opcode(9, i), '0', group, '1')
    opcode_encode_dict['v_relu' + i] = \
        set_meta(set_func_opcode(10, i), '0', group, '2')
    opcode_encode_dict['v_mul' + i] = \
        set_meta(set_func_opcode(11, i), '0', group, '3')
    opcode_encode_dict['v_mulacc' + i] = \
        set_meta(set_func_opcode(12, i), '0', group, '3')

for i in ['_hb', '_b', '_h', '_w']:
    opcode_encode_dict['v_sigmoid' + i] = \
        set_meta(set_func_opcode(13, i), '0', group, '4')
    opcode_encode_dict['v_tanh' + i] = \
        set_meta(set_func_opcode(14, i), '0', group, '4')
    opcode_encode_dict['v_exp' + i] = \
        set_meta(set_func_opcode(15, i), '0', group, '4')
    opcode_encode_dict['v_log' + i] = \
        set_meta(set_func_opcode(16, i), '0', group, '4')
    opcode_encode_dict['v_sqrt' + i] = \
        set_meta(set_func_opcode(17, i), '0', group, '4')
    opcode_encode_dict['v_fi2fi' + i] = \
        set_meta(set_func_opcode(18, i), '0', group, '4')

for i in ['', 'i']:
    for j in ['_f', '_hb', '_b', '_h', '_w']:
        opcode_encode_dict['v_div' + i + j] = \
            set_meta(set_func_opcode(19, j), set_imm_opcode(i), group, '2')

# group 110
group = '110'
for i in ['_f', '_hb', '_b', '_h', '_w']:
    opcode_encode_dict['v_cnv1d' + i] = \
        set_meta(set_func_opcode(0, i), '0', group, '0')
    opcode_encode_dict['v_cnv2d' + i] = \
        set_meta(set_func_opcode(1, i), '0', group, '1')
    opcode_encode_dict['v_maxpooling1d' + i] = \
        set_meta(set_func_opcode(2, i), '0', group, '2')
    opcode_encode_dict['v_maxpooling2d' + i] = \
        set_meta(set_func_opcode(3, i), '0', group, '2')

# group 110
group = '111'
for i in ['', 'i']:
    for j in ['_f', '_hb', '_b', '_h', '_w']:
        opcode_encode_dict['v_xor' + i + j] = \
            set_meta(set_func_opcode(0, j), set_imm_opcode(i), group, '0')
        opcode_encode_dict['v_or' + i + j] = \
            set_meta(set_func_opcode(1, j), set_imm_opcode(i), group, '0')
        opcode_encode_dict['v_and' + i + j] = \
            set_meta(set_func_opcode(2, j), set_imm_opcode(i), group, '0')
        opcode_encode_dict['v_not' + i + j] = \
            set_meta(set_func_opcode(3, j), set_imm_opcode(i), group, '0')

for i in ['', 'i']:
    for j in ['_hb', '_b', '_h', '_w']:
        opcode_encode_dict['v_shl' + i + j] = \
            set_meta(set_func_opcode(0, j), set_imm_opcode(i), group, '1')
        opcode_encode_dict['v_shr' + i + j] = \
            set_meta(set_func_opcode(1, j), set_imm_opcode(i), group, '1')
        opcode_encode_dict['v_shar' + i + j] = \
            set_meta(set_func_opcode(2, j), set_imm_opcode(i), group, '1')
        opcode_encode_dict['v_rol' + i + j] = \
            set_meta(set_func_opcode(3, j), set_imm_opcode(i), group, '1')
        opcode_encode_dict['v_ror' + i + j] = \
            set_meta(set_func_opcode(4, j), set_imm_opcode(i), group, '1')

if __name__ == '__main__':
    import pprint
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(reg_encode_dict)
    print('=' * 20)
    pp.pprint(aux_reg_encode_dict)
    print('=' * 20)
    pp.pprint(opcode_encode_dict)
