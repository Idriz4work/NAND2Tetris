import re
import logging
import memory_arithmetic.symbolvalues as s
import memory_arithmetic.arithmetic as arh
import memory_arithmetic.pushpop as pushpop
import programmControl.branches as branches, VM as vm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s -- %(message)s -- (%(asctime)s)')



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
jumptable = s.Jump

def functiondecider(validlines,file_path):
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
            branches.writeloops(ins,file_path)
            continue
        
        if gotosyntax.match(ins):
            logging.info("GOTO")
            branches.writegoto(ins,file_path)
            continue

        if ifsyntax.match(ins):
            logging.info("IF")
            # 1 statement before this ifgoto from the validlines
            symbol = saver[-1]
            symbol = jumptable.get_char(symbol)
            # if the previous line is not a operator (lt,gt,ect..) in the jumptable then it's simply JMP
            if symbol == "not found":
                symbol == "JMP"
            branches.writeifs(ins,symbol=symbol,file_path=file_path)
            continue

        if functionsyntax.match(ins):
            logging.info("FUNCTION")
            nVARS = ins[-1]
            vm.writefunctions(ins,nVARS,file_path)
            continue

        if returnsyntax.match(ins):
            lastvalue = saver[-1]
            logging.info("RETURN")
            vm.writereturns(ins,lastvalue,file_path)
            continue

        if callssyntax.match(ins):
            logging.info("CALL")
            nARGS = ins[-1]
            vm.writecalls(ins,nARGS,file_path)
            continue
    
        arithsyntax = None
        for i, name in enumerate(arithsyn):
            if name.match(ins):
                arithsyntax = arithsyn[i]
                break
        if arithsyntax:
            logging.info("arithmetic")
            arh.ArithmeticOperations(0,0,ins,file_path)

        push_match = None
        for i, pattern in enumerate(push_patterns):
            if pattern.match(ins):
                push_match = symbols[i]
                break
        
        if push_match:
            logging.info(f"push command: {push_match.name}")
            pushpop.pusher(ins, push_match,file_path)
            continue
        
        pop_match = None
        for i, pattern in enumerate(pop_patterns):
            if pattern.match(ins):
                pop_match = symbols[i]
                break
        
        if pop_match:
            logging.info(f"pop command: {pop_match.name}")
            pushpop.poper(ins, pop_match,file_path)
            continue    
        """saver is important to get 1 previus line in the validlines
        so we can update the if statements accordingly"""
        saver = []
        saver.append(ins)