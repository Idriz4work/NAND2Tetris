import os
import config
import re
import shutil
import logging
import argparse
import symbolvalues as s
import fileprep as f
import arithmetic as arh
import pushpop

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s -- %(message)s -- (%(asctime)s)')

# Global variables
config.inputfile = None
config.outputfile = None

# J keeps track of the address we are in static
j = 0

# Create instances
sp = s.stackPointer()
local = s.Local()
argument = s.Argument()
this = s.This()
that = s.That()
temp = s.Temp()
general = s.General()
static = s.Static()
stack = s.Stack()

# symbol classes
symbols = [sp, local, argument, this, that, temp, general, static, stack]
arithmeticslogics = ["add","sub","eq","lt","gt","or","and","neg","not"]
jump = s.Jump

def writeloops(value):
    parts = value.split()
    name = parts[1]
    with open(config.outputfile,'a') as asmfile:
        asmfile.write(f"""
// LOOP
({name})
""")

def writegoto(value):
    parts = value.split()
    name = parts[0]
    with open(config.outputfile,'a') as asmfile:
        asmfile.write(f"""
// goto 
@{name}
D;JMP
""")

def writeifs(value,symbol):
    parts = value.split()
    name = parts[1]
    # get the SP before the ifgoto and compare it to the Jump table
    with open(config.outputfile,'a') as asmfile:
        asmfile.write(f"""
// if statement
@{name}
D;{symbol}
""")


def writefunctions(value,nVARS):
    parts = value.split()
    pass

def writecalls(value,nARGS):
    parts = value.split()
    i = parts[-1]
    with open(config.outputfile,'a') as asmfile:
        asmfile.write(f""" // push return address
@returnaddress
D=A
@SP
A=M
D=M
// push LCL,ARG,THIS,THAT
@LCL
D=M
@ARG
D=M
@THIS
D=M
@THAT
D=M
// ARG = SP-5-nARGS
@5
M=A
@{i}
D=A
@SP
D=D+M
@ARG
D=A
// LCL = SP
@SP
D=A
@LCL
A=D
""")
        # goto {functionname}
        writegoto(parts[0])
        # insert labelname

def writereturns(value):
    parts = value.split()
    pass