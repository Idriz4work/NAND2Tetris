import os
import config
import re
import shutil
import logging
import argparse
import symbolvalues as s
import fileprep as f
import arithmetic as arh
import pushpop, branches

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s -- %(message)s -- (%(asctime)s)')

# Global variables
config.inputfile = None
config.outputfile = None

# J keeps track of the address we are in static
j = 0

# Create instances
jumptable = s.Jump()
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

# -------------------------- #
def writefunctions(value,nVARS):
    parts = value.split('.')
    name = parts[1]
    with open(config.outputfile,'a') as asmfile:
        asmfile.write(f"//function {name}\n@LCL\nD=M\n@{name}\nA=D")
        for i in nVARS:
            asmfile.write(f"""// nVARS
@0
D=A
@{i} // current number
A=M
M=D
@LCL
M=D




""")
            i += 1

def writecalls(value,nARGS):
    parts = value.split(r"\d")
    i = parts[-1]
    with open(config.outputfile,'a') as asmfile:
        asmfile.write(f""" // push return address {value}
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
        # writegoto(parts[0])
        # insert labelname

def writereturns(value):
    parts = value.split()
    pass


def functiondecider(validlines):
    # regex
    num = r"\d+"
    loopsyntax = re.compile(r"label [a-zA-Z]")
    gotosyntax = re.compile(r"goto [a-zA-Z]")
    ifsyntax = re.compile(r"if-goto [a-zA-Z]")

    functionsyntax = re.compile(r"function [a-zA-Z0-9]+\.[a-zA-Z0-9]+ \d+")
    callssyntax = re.compile(r"call [a-zA-Z0-9]+\.[a-zA-Z0-9]+ \d+")
    returnsyntax = re.compile(r"return")

    push_patterns = [re.compile(f"push {symbol.name} {num}") for symbol in symbols]
    pop_patterns = [re.compile(f"pop {symbol.name} {num}") for symbol in symbols]

    arithsyn = [re.compile(f"{symbol}") for symbol in arithmeticslogics]

    for ins in validlines:
        if loopsyntax.match(ins):
            logging.info("LOOP")
            branches.writeloops(ins)
            continue
        
        if gotosyntax.match(ins):
            logging.info("GOTO")
            branches.writegoto(ins)
            continue

        if ifsyntax.match(ins):
            logging.info("IF")
            # 1 statement before this ifgoto from the validlines
            symbol = saver[-1]
            symbol = jumptable.get_char(symbol)
            # if the previous line is not a operator (lt,gt,ect..) in the jumptable then it's simply JMP
            if symbol == "not found":
                symbol == "JMP"
            branches.writeifs(ins,symbol=symbol)
            continue

        if functionsyntax.match(ins):
            logging.info("FUNCTION")
            nVARS = ins[-1]
            writefunctions(ins,nVARS)
            continue

        if returnsyntax.match(ins):
            logging.info("RETURN")
            writereturns(ins)
            continue

        if callssyntax.match(ins):
            logging.info("CALL")
            nARGS = ins[-1]
            writecalls(ins,nARGS)
            continue
    
        arithsyntax = None
        for i, name in enumerate(arithsyn):
            if name.match(ins):
                arithsyntax = arithsyn[i]
                break
        if arithsyntax:
            logging.info("arithmetic")
            arh.ArithmeticOperations(0,0,ins)

        push_match = None
        for i, pattern in enumerate(push_patterns):
            if pattern.match(ins):
                push_match = symbols[i]
                break
        
        if push_match:
            logging.info(f"push command: {push_match.name}")
            pushpop.pusher(ins, push_match)
            continue
        
        pop_match = None
        for i, pattern in enumerate(pop_patterns):
            if pattern.match(ins):
                pop_match = symbols[i]
                break
        
        if pop_match:
            logging.info(f"pop command: {pop_match.name}")
            pushpop.poper(ins, pop_match)
            continue    
        """saver is important to get 1 previus line in the validlines
        so we can update the if statements accordingly"""
        saver = []
        saver.append(ins)


def main():
    # prepare variables & addreses in Asembly
    f.filepreparation()
    # go throu each line & remove whitespaces & comments
    validlines = []
    with open(config.inputfile, "r") as file:
        for line in file:
            line = line.strip()
            if not line.startswith("//") and line:
                validlines.append(line)
    # call the right function acording to the elements inside of config.inputfile
    functiondecider(validlines)
    
    # closing statement 
    with open(config.outputfile, "a") as asmfile:
        asmfile.write("//END OF FILE\n")
    dest = "output"
    if not os.path.exists(dest):
        os.mkdir(dest)
    shutil.move(config.outputfile, os.path.join(dest, os.path.basename(config.outputfile)))
    logging.critical("SUCCESS: translated VMcode into ASM\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", type=str, help="USAGE: [INPUT] [OUTPUT]")
    parser.add_argument("outputfile", type=str, help="USAGE: [INPUT] [OUTPUT]")
    args = parser.parse_args()
    
    config.inputfile = args.inputfile
    config.outputfile = args.outputfile
    
    main()
