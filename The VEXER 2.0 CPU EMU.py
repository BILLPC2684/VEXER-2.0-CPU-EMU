import time,os,sys,socket,threading,random
#from graphics import *
from _thread import *
#8-BIT SYSTEM
#7-BIT ROM SYSTEM
print("insert the filename of the ROM")
address=input()
file = open("ROMS/" + address + ".vex")
H=32#16
W=128#32
#win = GraphWin("VEXER 2.0 v1.2 CPU EMU",W,H)
#132x65
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
VIDEO=[]
loadedimage=[]
io=0
while io!=W:
    loadedimage+=0,
    io+=1
io2=0
print(loadedimage)
while io2!=H:
    VIDEO+=list(loadedimage)
    io2+=1

def line(x0, x1, y0, y1, color): # most code from Voltzlive
  dx = abs(x1-x0)
  if x0<x1 :
    sx = 1
  else:
    sx = -1
  dy = -abs(y1-y0)
  if y0<y1 :
    sy = 1
  else:
    sy = -1
  err = dx+dy
  e2 = 0
  while True:
    X=x0
    Y=y0
    if not(Y<0 or X<0 and Y>H-1 or X>W-1):
        if W*Y-(W*Y>0) >= 0:
            VIDEO[(W*Y-(W*Y>0))+X+(1*Y>0)]=color
    if x0==x1 and y0==y1:
        break
    e2 = 2*err
    if e2 >= dy:
      err += dy
      x0 += sx
    if e2 <= dx: 
      err += dx
      y0 += sy

I=0
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
    time.sleep(0.01)#.5)
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
        elif int(data[1]) == 1:
         print(hex(REGS[int(data[2])]))
        PC+=1
    if data[0] == "JMP" or data[0] == "6":
        if int(data[1]) == 0:
            PC=int(data[2])-1
        elif int(data[1]) == 1:
            PC=REGS[int(data[2])]-1
    if data[0] == "ifF" or data[0] == "7":
        if data[1] == "0":
            if REGS[5] == 0:
                PC=PC+1
            else:
                PC=PC+2
        if data[1] == "1":
            if REGS[5] == 1:
                PC=PC+1
            else:
                PC=PC+2
        if data[1] == "=" or data[1] == "2":
            if REGS[5] == int(data[2]):
                PC=PC+1
            else:
                PC=PC+2
        if data[1] == "<" or data[1] == "3":
            if REGS[5] < int(data[2]):
                PC=PC+1
            else:
                PC=PC+2
        if data[1] == ">" or data[1] == "4":
            if REGS[5] > int(data[2]):
                PC=PC+1
            else:
                PC=PC+2

    if data[0] == "RAM" or data[0] == "9":
        if data[1] == "setPos":
            RAMPOS=int(data[2])
        elif data[1] == "setPosREG":
            RAMPOS=REGS[int(data[2])]
        elif data[1] == "write":
            RAM[RAMPOS]=REGS[int(data[2])]
        elif data[1] == "read":
            REGS[int(data[2])]=RAM[RAMPOS]
        PC+=1
    if data[0] == "SCREEN" or data[0] == "A":
        if data[1] == "SetX" or data[1] == "0":
            X=int(data[2])
        elif data[1] == "SetY" or data[1] == "1":
            Y=int(data[2])
        elif data[1] == "SetX2" or data[1] == "2":
            X2=int(data[2])
        elif data[1] == "SetY2" or data[1] == "3":
            Y2=int(data[2])
        elif data[1] == "REGSetX" or data[1] == "4":
            X=REGS[int(data[2])]
        elif data[1] == "REGSetY" or data[1] == "5":
            Y=REGS[int(data[2])]
        elif data[1] == "REGSetX2" or data[1] == "6":
            X2=REGS[int(data[2])]
        elif data[1] == "REGSetY2" or data[1] == "7":
            Y2=REGS[int(data[2])]
        elif data[1] == "plot" or data[1] == "8":
            if not(Y<0 or X<0 and Y>H-1 or X>W-1):
                if W*Y-(W*Y>0) >= 0:
                    VIDEO[(W*Y-(W*Y>0))+X+(1*Y>0)]=int(data[2])
        elif data[1] == "plotREGcolor" or data[1] == "9":
            if not(Y<0 or X<0 and Y>H-1 or X>W-1):
                if W*Y-(W*Y>0) >= 0:
                    VIDEO[(W*Y-(W*Y>0))+X+(1*Y>0)]=REGS[int(data[2])]
        elif data[1] == "Line" or data[1] == "A":
            #(x-y,x2-y2)
            line(X,X2,Y,Y2,int(data[2]))
        elif data[1] == "update" or data[1] == "B":
            sysio=0
            io=0
            sys.stdout.write("/")
            while io!=W:
                sys.stdout.write("-")
                io+=1
            sys.stdout.write("\\\n")
            io2=0
            while io2!=H+1:
                if io2!=0:
                    sys.stdout.write("|")
                    while io!=W:
                        #print(io2)
                        if io2!=H+1:
                            #print(io2)
                            if VIDEO[sysio] == 0:
                                sys.stdout.write(" ")
                            elif VIDEO[sysio] == 1:
                                sys.stdout.write("█")
                            elif VIDEO[sysio] == 2:
                                sys.stdout.write("▓")
                            elif VIDEO[sysio] == 3:
                                sys.stdout.write("▒")
                            elif VIDEO[sysio] == 4:
                                sys.stdout.write("░")
                            sysio+=1
                            io+=1
                if io2!=0:
                    sys.stdout.write("|\n")
                io2+=1
                io=0
            sys.stdout.write("\\")
            io=0
            while io!=W:
                sys.stdout.write("-")
                io+=1
            sys.stdout.write("/\n")
        PC+=1
