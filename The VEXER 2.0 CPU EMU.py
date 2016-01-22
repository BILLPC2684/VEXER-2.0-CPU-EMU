import time,os,sys,socket
#12-BIT ROM SYSTEM
#ROM 8x8(64)
print("insert the filename of the ROM")
address=input()
file = open("ROMS/" + address + ".vex")
#               vFlags
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
    if data[0] == "systemInput":
        REGS[int(data[2])]=int(data[1])
        PC+=1
    if data[0] == "userInput":
        REGS[int(data[1])]=int(input())
        PC+=1
    if data[0] == "setALU":
        if data[1] == "A" or data[1] == "a":
            ALUA=REGS[int(data[2])]
        elif data[1] == "B" or data[1] == "b":
            ALUB=REGS[int(data[2])]
        PC+=1
    if data[0] == "ALU":
        if data[1] == "add" or data[1] == "ADD":
            REGS[5]=0
            REGS[int(data[2])]=ALUA+ALUB
            if REGS[int(data[2])] > 0xFF:
                REGS[int(data[2])]-=0xFF
        elif data[1] == "adc" or data[1] == "ADC":
            REGS[5]=0
            REGS[int(data[2])]=ALUA+ALUB
            if REGS[int(data[2])] > 0xFF:
                REGS[int(data[2])]-=0xFF
                REGS[5]=1
        elif data[1] == "sub" or data[1] == "SUB":
            REGS[5]=1
            REGS[int(data[2])]=ALUA-ALUB
            if REGS[int(data[2])] < -0xFF:
                REGS[int(data[2])]+=0xFF
        elif data[1] == "sbc" or data[1] == "SBC":
            REGS[5]=1
            REGS[int(data[2])]=ALUA-ALUB
            if REGS[int(data[2])] < -0xFF:
                REGS[int(data[2])]+=0xFF
                REGS[5]=0
        elif data[1] == "shl" or data[1] == "SHL":
            ALUC=ALUA*2
            if ALUC > 0xFF:
                ALUC-=0xFF
            REGS[int(data[2])]=ALUC
        elif data[1] == "shr" or data[1] == "SHR":
            ALUC=ALUA/2
            if ALUC < 0xFF:
                ALUC+=0xFF
            REGS[int(data[2])]=ALUC
        elif data[1] == "and" or data[1] == "AND":
            ALUC=ALUA&ALUB
            REGS[int(data[2])]=ALUC
        elif data[1] == "or" or data[1] == "OR":
            ALUC=ALUA|ALUB
            REGS[int(data[2])]=ALUC
        elif data[1] == "xor" or data[1] == "XOR":
            ALUC=ALUA|ALUB
            ALUC=ALUA&ALUB
            REGS[int(data[2])]=ALUC
        elif data[1] == "inv" or data[1] == "INV":
            ALUC=-ALUA
            REGS[int(data[2])]=ALUC
        PC+=1
    if data[0] == "print":
        print(REGS[int(data[1])])
        PC+=1
    if data[0] == "JMP":
        if int(data[1]) == 0:
            PC=int(data[2])-1
        if int(data[1]) == 1:
            PC=REGS[int(data[2])]-1
    if data[0] == "ifF":
        if REGS[5] == int(data[1]):
            PC=PC+1
        else:
            PC=PC+2