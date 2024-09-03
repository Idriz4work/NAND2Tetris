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
import branches as b

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

def callfunction(validlines):
    # regex
    num = r"\d+"
    loopsyntax = re.compile(r"label [a-zA-Z]")
    gotosyntax = re.compile(r"goto [a-zA-Z]")
    ifsyntax = re.compile(r"if-goto [a-zA-Z]")

    functionsyntax = re.compile(r"function \d+ \d+")
    callssyntax = re.compile(r"call \d+ \d+")
    returnsyntax = re.compile(r"return")

    push_patterns = [re.compile(f"push {symbol.name} {num}") for symbol in symbols]
    pop_patterns = [re.compile(f"pop {symbol.name} {num}") for symbol in symbols]

    arithsyn = [re.compile(f"{symbol}") for symbol in arithmeticslogics]

    for ins in validlines:

        if loopsyntax.match(ins):
            logging.info("LOOP")
            b.writeloops(ins)
            continue
        
        if gotosyntax.match(ins):
            logging.info("GOTO")
            b.writegoto(ins)
            continue

        if ifsyntax.match(ins):
            logging.info("IF")
            b.writeifs(ins)
            continue

        if functionsyntax.match(ins):
            logging.info("FUNCTION")
            b.writefunctions(ins)
            continue

        if returnsyntax.match(ins):
            logging.info("RETURN")
            b.writereturns(ins)
            continue

        if callssyntax.match(ins):
            logging.info("CALL")
            b.writecalls(ins)
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
