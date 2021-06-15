from constants import *


def hex2mips(cmd: str) -> str:
    if len(cmd) != 32:
        raise Exception('{} is illegal!'.format(cmd))

    op_ = cmd[:6]
    op = opcode_dict[op_]
    result = 'NONE'
    if op == 'R':
        rs_, rt_, rd_, shamt_, funct_ = cmd[6:11], cmd[11:16], cmd[16:21], cmd[21:26], cmd[26:]
        rs = reg_dict[rs_]
        rt = reg_dict[rt_]
        rd = reg_dict[rd_]
        shamt = int(eval('0b{}'.format(shamt_)))
        funct = funct_dict[funct_]
        if funct in ['add', 'addu', 'sub', 'subu', 'or', 'xor', 'nor', 'slt', 'sltu']:
            result = '{} {}, {}, {}'.format(funct, rd, rs, rt)
        elif funct in ['sll', 'srl', 'sra']:
            result = '{} {}, {}, {}'.format(funct, rd, rt, shamt)
        elif funct in ['sllv', 'srlv', 'srav']:
            result = '{} {}, {}, {}'.format(funct, rd, rt, rs)
        elif funct in ['mult', 'multu', 'div', 'divu']:
            result = '{} {}, {}'.format(funct, rs, rt)
        elif funct in ['jr', 'jalr']:
            result = '{} {}'.format(funct, rs)
    elif op in ['j', 'jal']:
        addr = hex(eval('0b{}{}00'.format(PCaddr, cmd[-26:])))
        result = '{} {}'.format(op, addr)
    elif op == 'F':
        raise Exception('F is not defined!')
    elif op == 'bltz/bgez':
        rs_ = cmd [6:11]
        rt_ = cmd[11:16]
        rs = reg_dict[rs_]
        addr_bin = cmd[-16:]
        addr = int(eval('0b{}'.format(addr_bin)))
        if addr_bin[0] == '1':
            addr = ~addr ^ 0xFFFF
        if rt_ == '00000':
            op = 'bltz'
        elif rt_ == '00001':
            op = 'bgez'
        else:
            raise Exception('bltz/bgez with illegal rt = {} !'.format(rt_))
        result = '{} {}, {}'.format(op, rs, addr << 2)
    else:
        rs_, rt_, imm_ = cmd[6:11], cmd[11:16], cmd[16:]
        rs = reg_dict[rs_]
        rt = reg_dict[rt_]
        imm = int(eval('0b{}'.format(imm_)))
        if imm_[0] == '1':
            imm = ~imm ^ 0xFFFF
        if op in ['beq', 'bne']:
            addr = int(imm << 2)
            result = '{} {}, {}, {}'.format(op, rs, rt, addr)
        elif op in ['addi', 'addiu', 'slti', 'sltiu', 'andi', 'ori', 'xori']:
            result = '{} {}, {}, {}'.format(op, rt, rs, imm)
        elif op == 'mul':
            rd_ = cmd[16:21]
            rd = reg_dict[rd_]
            result = '{} {}, {}, {}'.format(op, rd, rs, rt)
        elif op in ['lw', 'sw', 'lh', 'lb', 'lhu', 'lbu', 'sb', 'sh']:
            result = '{} {}, {}({})'.format(op, rt, imm, rs)
    return result

if __name__ == '__main__':
    with open('hex.txt', 'r') as fr, open('hex_result.txt', 'w') as fw:
        sentences = fr.readlines()
        for hex_cmd in sentences:
            binary_cmd = bin(eval(hex_cmd.rstrip('\n')))[2:].zfill(32)
            str_cmd = hex2mips(binary_cmd)
            fw.write(str_cmd + '\n')
