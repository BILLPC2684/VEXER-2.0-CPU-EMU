import time,os,sys,socket,threading,random
from _thread import *
#8-BIT SYSTEM
#6-BIT ROM SYSTEM(64)
print("insert the filename of the ROM")
address=input()
file = open("ROMS/" + address + ".vex")
#"VEXER 2.0 v1.2 CPU EMU"
#132x65
H=32
W=12
screensize=H*W
#OPCODES:
#1#setALU <A/B> <REGID>
#2#ALU <ADD/SUB/ADC/SBC/OR/AND/XOR/SHL/SHR/RNG/RNGA-B/</=/>/INV> <REGID(out)>
#3#systemInput <REGID(out)> <VALUE>
#4#userInput <REGID(out)>
#5#print <0(print in DEC),1(print in HEX)> <REGID>
#6#JMP PC=<REGID>
#7#ifF F(Flag)==<ARG> (if true PC+1 if false PC+2)
#8#RAM <setPos/setPosREG/write/read> <setPos:data/REGID(in/out)>
#9#SCREEN <SetX,SetY,SetX2,SetY2,WritePixel,ReadPixel,Line(x-y,x2-y2)> <REGID(in/out)>
#A#
#B#
#C#
#D#
#E#
#F#
#    $A$B$C#D$E$F$G$H
REGS=[0,0,0,0,0,0,0,0]
# ID: 0 1 2 3 4 5 6 7
functionREGS=[0,0,0,0,0,0,0,0]
#         ID: 0 1 2 3 4 5 6 7
X=0
Y=0
X2=0
Y2=0
VIDEO={}
TEST="["
I=0
while I != W:
    TEST+="0,"
    I+=1
TEST+="0]"
I=0
while I != H:
    VIDEO[I]=(TEST)
    I+=1
PC=0x00
RAM=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
RAMPOS=0x00
tempID=0
SP=0x00
STACK=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
ALUA=0x00
ALUB=0x00
ALUC=0x00
RC=0
debug = 0
ROM={}
for i in file:
    ROM[RC]=i
    RC+=1
while True:
    time.sleep(0.5)
    data=str.split(ROM[PC])
    if debug == 1:
        print(PC,data,ALUA,ALUB,ALUC,REGS,functionREGS,STACK)
    if data[0] == "systemInput" or data[0] == "3":
        REGS[int(data[2])]=int(data[1])
        PC+=1
    if data[0] == "userInput" or data[0] == "4":
        inpdata=int(input())
        if inpdata > 0xFF:
            inpdata-=0xFF
        REGS[int(data[1])]=inpdata
        PC+=1
    if data[0] == "setALU" or data[0] == "1":
        if data[1] == "A" or data[1] == "a" or data[1] == "0":
            ALUA=REGS[int(data[2])]
        elif data[1] == "B" or data[1] == "b" or data[1] == "1":
            ALUB=REGS[int(data[2])]
        PC+=1
    if data[0] == "ALU" or data[0] == "2":
        if data[1] == "add" or data[1] == "ADD" or data[1] == "0":
            REGS[5]=0
            ALUC=ALUA+ALUB
            if ALUC > 0xFF:
                ALUC-=0xFF
            REGS[int(data[2])]=ALUC
        elif data[1] == "adc" or data[1] == "ADC" or data[1] == "1":
            REGS[5]=0
            ALUC=ALUA+ALUB
            if ALUC > 0xFF:
                ALUC-=0xFF
                REGS[5]=1
            REGS[int(data[2])]=ALUC
        elif data[1] == "sub" or data[1] == "SUB" or data[1] == "2":
            REGS[5]=1
            ALUC=ALUA-ALUB
            if ALUC < -0xFF:
                ALUC+=0xFF
            REGS[int(data[2])]=ALUC
        elif data[1] == "sbc" or data[1] == "SBC" or data[1] == "3":
            REGS[5]=1
            ALUC=ALUA-ALUB
            if ALUC < -0xFF:
                ALUC+=0xFF
                REGS[5]=0
            REGS[int(data[2])]=ALUC
        elif data[1] == "shl" or data[1] == "SHL" or data[1] == "4":
            ALUC=ALUA*2
            if ALUC > 0xFF:
                ALUC-=0xFF
            REGS[int(data[2])]=ALUC
        elif data[1] == "shr" or data[1] == "SHR" or data[1] == "5":
            ALUC=ALUA/2
            if ALUC < 0xFF:
                ALUC+=0xFF
            REGS[int(data[2])]=ALUC
        elif data[1] == "and" or data[1] == "AND" or data[1] == "6":
            ALUC=ALUA&ALUB
            REGS[int(data[2])]=ALUC
        elif data[1] == "or" or data[1] == "OR" or data[1] == "7":
            ALUC=ALUA|ALUB
            REGS[int(data[2])]=ALUC
        elif data[1] == "xor" or data[1] == "XOR" or data[1] == "8":
            ALUC=ALUA|ALUB
            ALUC=ALUA&ALUB
            REGS[int(data[2])]=ALUC
        elif data[1] == "<" or data[1] == "9":
            if ALUA<ALUB:
                REGS[5]=2
        elif data[1] == ">" or data[1] == "A":
            if ALUA>ALUB:
                REGS[5]=3
        elif data[1] == "=" or data[1] == "B":
            if ALUA==ALUB:
                REGS[5]=4
        elif data[1] == "inv" or data[1] == "INV" or data[1] == "C":
            ALUC=-ALUA
            REGS[int(data[2])]=ALUC
        elif data[1] == "rng" or data[1] == "RNG" or data[1] == "D":
            REGS[int(data[2])]=random.randint(0,255)
        elif data[1] == "rngA-B" or data[1] == "RNGA-B" or data[1] == "e":
            REGS[int(data[2])]=random.randint(ALUA,ALUB)
        PC+=1
    if data[0] == "print" or data[0] == "5":
        if int(data[1]) == 0:
         print(REGS[int(data[2])])
        if int(data[1]) == 1:
         print(hex(REGS[int(data[2])]))
        PC+=1
    if data[0] == "JMP" or data[0] == "6":
        if int(data[1]) == 0:
            PC=int(data[2])-1
        if int(data[1]) == 1:
            PC=REGS[int(data[2])]-1
    if data[0] == "ifF" or data[0] == "7":
        if REGS[5] == int(data[1]):
            PC=PC+1
        else:
            PC=PC+2
    if data[0] == "RAM" or data[0] == "9":
        if data[1] == "setPos":
            RAMPOS=int(data[2])
        if data[1] == "setPosREG":
            RAMPOS=REGS[int(data[2])]
        if data[1] == "write":
            RAM[RAMPOS]=REGS[int(data[2])]
        if data[1] == "read":
            REGS[int(data[2])]=RAM[RAMPOS]
    if data[0] == "SCREEN" or data[0] == "A":
        if data[1] == "SetX":
            X=data[2]
        if data[1] == "SetY":
            Y=data[2]
        if data[1] == "SetX2":
            X2=data[2]
        if data[1] == "SetY2":
            Y2=data[2]
        if data[1] == "WritePixel":
            if X >= 0 and Y >= 0 and X <= W and Y <= H:
                VIDEO[X,Y]=data[2]
        if data[1] == "Line":
            #(x-y,x2-y2)
            while X != X2 and Y!=Y2:
                if X >= 0 and Y >= 0 and X <= W and Y <= H:
                    VIDEO[X,Y]=data[2]
                if X > X2:
                    X-=1
                elif X < X2:
                    X+=1
                if Y > Y2:
                    Y-=1
                elif Y < Y2:
                    Y+=1
        if data[1] == "update":
            while io!=100:
                print("")
            sys.stdout.write("/")
            while io!=W-2:
                sys.stdout.write("-")
            sys.stdout.write("\\")
            while io2!=H:
                sys.stdout.write("|")
                while io!=W-2:
                    sys.stdout.write(VIDEO[io2][io])
                sys.stdout.write("|")
            sys.stdout.write("\\")
            while io!=W-2:
                sys.stdout.write("-")
            sys.stdout.write("/")


