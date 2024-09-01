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

def main():
    f.filepreparation()

    # regex
    num = r"\d+"
    push_patterns = [re.compile(f"push {symbol.name} {num}") for symbol in symbols]
    pop_patterns = [re.compile(f"pop {symbol.name} {num}") for symbol in symbols]

    staticpattern = [re.compile(f"{symbol.name}") for symbol in symbols]
    add = re.compile(r"add")
    sub = re.compile(r"sub")

    validlines = []
    with open(config.inputfile, "r") as file:
        for line in file:
            line = line.strip()
            if not line.startswith("//") and line:
                validlines.append(line)


    for ins in validlines:

        topstack = None
        beforeTopstack = None
        for i, pattern in enumerate(staticpattern):
            if pattern.match("constant"):
                topstack = symbols[i]
                break
        for i, pattern in enumerate(staticpattern):
            if pattern.match("constant"):
                beforeTopstack = symbols[i]
                break

        if add.match(ins) or sub.match(ins):
            logging.info("arithmetic")
            # Find the top two non-constant symbols
            non_constants = [symbol for symbol in reversed(symbols) if not re.match(r"constant", symbol.name)]
            
            if len(non_constants) >= 2:
                topstack = non_constants[0]
                beforeTopstack = non_constants[1]
                
                logging.info(f"FOUND VALUES: {topstack.name}, {beforeTopstack.name}")
                
                # Pop the top two values from the stack
                pushpop.poper(topstack, topstack.name)
                pushpop.poper(beforeTopstack, beforeTopstack.name)
                
                # Perform arithmetic operation
                arh.ArithmeticOperations(ins, topstack, beforeTopstack)
            else:
                logging.error("NOT ENOUGH NON-CONSTANT VALUES FOUND")
                return
        
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
