from constants import *

PCaddr = '0000'


def R_generate(funct, rs='$0', rt='$0', rd='$0', shamt='00000'):
    return '000000' + reg_dict_r[rs] + reg_dict_r[rt] + reg_dict_r[rd] + shamt + funct_dict_r[funct]


def I_generate(op, rs, rt, imm):
    return opcode_dict_r[op] + reg_dict_r[rs] + reg_dict_r[rt] + imm[2:]


def J_generate(op, imm):
    return opcode_dict_r[op] + imm[2:]


def mips2hex(cmd: str) -> str:
    op_func = cmd.partition(' ')[0]
    op_items = cmd.partition(' ')[2].split(',')
    op_items = [item.lstrip(' ').rstrip(' ') for item in op_items]
    result = 'NONE'

    if op_func in ['lw', 'sw', 'lh', 'lb', 'lhu', 'lbu', 'sb', 'sh']:
        rt_ = op_items[0]
        imm_ = op_items[1].partition('(')[0]
        rs_ = op_items[1].partition('(')[2].rstrip(')')
        if eval(imm_) >= 0:
            imm_ = '0b' + bin(eval(imm_))[2:].zfill(16)
        else:
            imm_ = bin(2 ** 16 + eval(imm_))
        result = I_generate(op=op_func, rs=rs_, rt=rt_, imm=imm_)

    elif op_func == 'mul':
        rd_, rs_, rt_ = op_items[0], op_items[1], op_items[2]
        result = opcode_dict_r[op_func] + reg_dict_r[rs_] + reg_dict_r[rt_] + reg_dict_r[rd_] + '0' * 5 + '000010'

    elif op_func in ['add', 'addu', 'sub', 'subu', 'or', 'xor', 'nor', 'slt', 'sltu']:
        rs_, rt_, rd_ = op_items[1], op_items[2], op_items[0]
        result = R_generate(rs=rs_, rt=rt_, rd=rd_, funct=op_func)

    elif op_func in ['sll', 'srl', 'sra']:
        rt_, rd_, shamt_ = op_items[1], op_items[0], op_items[2]
        result = R_generate(rt=rt_, rd=rd_, funct=op_func, shamt=shamt_)

    elif op_func in ['sllv', 'srlv', 'srav']:
        rs_, rt_, rd_ = op_items[2], op_items[1], op_items[0]
        result = R_generate(rs=rs_, rt=rt_, rd=rd_, funct=op_func)

    elif op_func in ['mult', 'multu', 'div', 'divu']:
        rs_, rt_ = op_items[0], op_items[1]
        result = R_generate(rs=rs_, rt=rt_, funct=op_func)

    elif op_func in ['jr', 'jalr']:
        rs_ = op_items[0]
        result = R_generate(rs=rs_, funct=op_func)

    elif op_func in ['j', 'jal']:
        label = '0b' + bin(eval(op_items[0]) >> 2)[2:].zfill(26)
        result = J_generate(op=op_func, imm=label)

    elif op_func in ['bltz', 'bgez']:
        rs_ = op_items[0]
        label_ = op_items[1]
        if eval(label_) >= 0:
            label = '0b' + bin(eval(label_))[2:].zfill(16)
        else:
            label = bin(2 ** 16 + eval(label_))
        if op_func == 'bltz':
            rt_ = '00000'
        else:
            rt_ = '00001'
        result = I_generate(op=op_func, rs=rs_, rt=rt_, imm=label)

    else:
        imm_ = op_items[2]
        if eval(imm_) >= 0:
            imm_ = '0b' + bin(eval(imm_))[2:].zfill(16)
        else:
            imm_ = bin(2 ** 16 + eval(imm_))
        if op_func in ['beq', 'bne']:
            rs_, rt_ = op_items[0], op_items[1]
            result = I_generate(op=op_func, rs=rs_, rt=rt_, imm=imm_)

        elif op_func in ['addi', 'addiu', 'slti', 'sltiu', 'andi', 'ori', 'xori']:
            rt_, rs_ = op_items[0], op_items[1]
            result = I_generate(op=op_func, rs=rs_, rt=rt_, imm=imm_)

    if len(result) == 32:
        return '0x' + str(hex(int(result, 2)))[2:].zfill(8)
    else:
        raise Exception('binary {} is illegal with command {}!'.format(result, cmd))

if __name__ == '__main__':
    with open('code.txt', 'r') as fr, open('code_result.txt', 'w') as fw:
        sentences = fr.readlines()
        for str_cmd in sentences:
            binary_cmd = mips2hex(str_cmd.rstrip('\n'))
            fw.write(binary_cmd + '\n')

