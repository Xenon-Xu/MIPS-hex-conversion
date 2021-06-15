# MIPS-hex-conversion
MIPS-hex-conversion (python) realize the conversion between MIPS assembly and machine code.

**supported MIPS assembly:** (in constant.py)
```opcode_dict = {
    '000000': 'R',
    '000001': 'bltz/bgez',
    '000010': 'j',
    '000011': 'jal',
    '000100': 'beq',
    '000101': 'bne',
    '001000': 'addi',
    '001001': 'addiu',
    '001010': 'slti',
    '001011': 'sltiu',
    '001100': 'andi',
    '001101': 'ori',
    '001110': 'xori',
    '001111': 'lui',
    '011100': 'mul',
    '100000': 'lb',
    '100001': 'lh',
    '100011': 'lw',
    '100100': 'lbu',
    '100101': 'lhu',
    '101000': 'sb',
    '101001': 'sh',
    '101011': 'sw'
}

funct_dict = {
    '000000': 'sll',
    '000010': 'srl',
    '000011': 'sra',
    '000100': 'sllv',
    '000110': 'srlv',
    '000111': 'srav',
    '001000': 'jr',
    '001001': 'jalr',
    '011000': 'mult',
    '011001': 'multu',
    '011010': 'div',
    '011011': 'divu',
    '100000': 'add',
    '100001': 'addu',
    '100010': 'sub',
    '100011': 'subu',
    '100100': 'and',
    '100101': 'or',
    '100110': 'xor',
    '100111': 'nor',
    '101010': 'slt',
    '101011': 'sltu'
}

reg_dict = {
    '00000': '$0',
    '00001': '$at',
    '00010': '$v0',
    '00011': '$v1',
    '00100': '$a0',
    '00101': '$a1',
    '00110': '$a2',
    '00111': '$a3',
    '01000': '$t0',
    '01001': '$t1',
    '01010': '$t2',
    '01011': '$t3',
    '01100': '$t4',
    '01101': '$t5',
    '01110': '$t6',
    '01111': '$t7',
    '10000': '$s0',
    '10001': '$s1',
    '10010': '$s2',
    '10011': '$s3',
    '10100': '$s4',
    '10101': '$s5',
    '10110': '$s6',
    '10111': '$s7',
    '11000': '$t8',
    '11001': '$t9',
    '11010': '$k0',
    '11011': '$k1',
    '11100': '$gp',
    '11101': '$sp',
    '11110': '$fp',
    '11111': '$ra',
}
```

## hex2mips.py
Converse mechine code (hex) in file 'hex.txt' into MIPS assembly in file 'hex_result.txt'.

**example**

hex.txt

```
0x20080000
0x20090001
0x0089502A
0x15400003
0x01094020
0x21290002
0x08100002
0x01001020
0x03E00008
```

hex_result.txt

```
addi $t0, $0, 0
addi $t1, $0, 1
slt $t2, $a0, $t1
bne $t2, $0, 12
add $t0, $t0, $t1
addi $t1, $t1, 2
j 0x400008
add $v0, $t0, $0
jr $ra
```


## mips2hex.py
Converse MIPS assembly in file 'code.txt' into mechine code (hex) in file 'code_result.txt'.

**example**

code.txt

```
addi $sp, $sp, -4
sw $ra, 0($sp)
addi $t0, $0, 15
sw $t0, 0x8000($gp)
addi $a1, $0, 27
sw $a1, 0x8004($gp)
lw $a0, 0x8000($gp)
jal 0x40002c
lw $ra, 0($sp)
addi $sp, $sp, 4
jr $ra
slt $v0, $a1, $a0
jr $ra
```

code_result.txt

```
0x23bdfffc
0xafbf0000
0x2008000f
0xaf888000
0x2005001b
0xaf858004
0x8f848000
0x0c10000b
0x8fbf0000
0x23bd0004
0x03e00008
0x00a4102a
0x03e00008
```

## PCaddr
The highest 4 bits of the PC pointer's initial value.

`PCaddr = 0b0000 # in default`
