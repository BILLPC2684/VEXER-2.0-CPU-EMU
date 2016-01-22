import time,os,sys,socket,threading
from _thread import *
#12-BIT ROM SYSTEM
#ROM 6-bit(64)
print("insert the filename of the ROM")
address=input()
file = open("ROMS/" + address + ".vex")
#"VEXER 2.0 v1.2 CPU EMU"
#132x65
screensize=132*65
#    $A$B$C#D$E$F$G$H
REGS=[0,0,0,0,0,0,0,0]
# ID: 0 1 2 3 4 5 6 7
PC=0x00
RAM=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
RAMPOS=0x00
SP=0x00
STACK={}
ALUA=0x00
ALUB=0x00
ALUC=0x00
RC=0
ROM={}
for i in file:
    ROM[RC]=i
    RC+=1
while True:
    time.sleep(0.5)
    data=str.split(ROM[PC])
    #print(PC,data,ALUA,ALUB,ALUC,REGS,STACK)
    #print("["+str(REGS[5])+"]")
    if data[0] == "systemInput" or data[0] == 0x3:
        REGS[int(data[2])]=int(data[1])
        PC+=1
    if data[0] == "userInput" or data[0] == 0x4:
        REGS[int(data[1])]=int(input())
        PC+=1
    if data[0] == "setALU" or data[0] == 0x1:
        if data[1] == "A" or data[1] == "a" or data[1] == 0x0:
            ALUA=REGS[int(data[2])]
        elif data[1] == "B" or data[1] == "b" or data[1] == 0x1:
            ALUB=REGS[int(data[2])]
        PC+=1
    if data[0] == "ALU" or data[0] == 0x2:
        if data[1] == "add" or data[1] == "ADD" or data[1] == 0x0:
            REGS[5]=0
            ALUC=ALUA+ALUB
            if ALUC > 0xFF:
                ALUC-=0xFF
            REGS[int(data[2])]=ALUC
        elif data[1] == "adc" or data[1] == "ADC" or data[1] == 0x1:
            REGS[5]=0
            ALUC=ALUA+ALUB
            if ALUC > 0xFF:
                ALUC-=0xFF
                REGS[5]=1
            REGS[int(data[2])]=ALUC
        elif data[1] == "sub" or data[1] == "SUB" or data[1] == 0x2:
            REGS[5]=1
            ALUC=ALUA-ALUB
            if ALUC < -0xFF:
                ALUC+=0xFF
            REGS[int(data[2])]=ALUC
        elif data[1] == "sbc" or data[1] == "SBC" or data[1] == 0x3:
            REGS[5]=1
            ALUC=ALUA-ALUB
            if ALUC < -0xFF:
                ALUC+=0xFF
                REGS[5]=0
            REGS[int(data[2])]=ALUC
        elif data[1] == "shl" or data[1] == "SHL" or data[1] == 0x4:
            ALUC=ALUA*2
            if ALUC > 0xFF:
                ALUC-=0xFF
            REGS[int(data[2])]=ALUC
        elif data[1] == "shr" or data[1] == "SHR" or data[1] == 0x5:
            ALUC=ALUA/2
            if ALUC < 0xFF:
                ALUC+=0xFF
            REGS[int(data[2])]=ALUC
        elif data[1] == "and" or data[1] == "AND" or data[1] == 0x6:
            ALUC=ALUA&ALUB
            REGS[int(data[2])]=ALUC
        elif data[1] == "or" or data[1] == "OR" or data[1] == 0x7:
            ALUC=ALUA|ALUB
            REGS[int(data[2])]=ALUC
        elif data[1] == "xor" or data[1] == "XOR" or data[1] == 0x8:
            ALUC=ALUA|ALUB
            ALUC=ALUA&ALUB
            REGS[int(data[2])]=ALUC
        elif data[1] == "inv" or data[1] == "INV" or data[1] == 0x9:
            ALUC=-ALUA
            REGS[int(data[2])]=ALUC
        PC+=1
    if data[0] == "print" or data[0] == 0x5:
        print(REGS[int(data[1])])
        PC+=1
    if data[0] == "JMP" or data[0] == 0x6:
        if int(data[1]) == 0:
            PC=int(data[2])-1
        if int(data[1]) == 1:
            PC=REGS[int(data[2])]-1
    if data[0] == "ifF" or data[0] == 0x7:
        if REGS[5] == int(data[1]):
            PC=PC+1
        else:
            PC=PC+2