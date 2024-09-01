import config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s -- %(message)s -- (%(asctime)s)')

# J keeps track of the address we are in static
j = 0

def ArithmeticOperations(topstack,beforetopstack,operator):
    logging.critical("starting arithmetic operations")
    with open(config.outputfile,"w") as asmfile:
        if operator == "add":
            logging.info("ADD")
            result = topstack + beforetopstack 
            asmfile.write(f""" // add {topstack} + {beforetopstack}
@{result}
D=A
@SP
A=M
M=D
@SP
M=M+1 // SP++
""")
            
        if operator == "sub":
            logging.info("SUB")
            result = topstack - beforetopstack 
            asmfile.write(f""" // add {topstack} - {beforetopstack}
@{result}
D=A
@SP
A=M
M=D
@SP
M=M+1 // SP++
""")
        if operator == "neg":
            logging.info("NEG")
            asmfile.write(f""" // neg {topstack}
@-{topstack}
D=A
@SP
A=M
M=D
@SP
M=M+1 // SP++
""")
        if operator == "eq":
            logging.info("EQ")
            if topstack == beforetopstack:
                result = "true"
            else:
                result == "false"
            asmfile.write(f""" // eq : {topstack} ? {beforetopstack}
@{result}
D=A
@SP
A=M
M=D
@SP
M=M+1 // SP++
""")
        if operator == "or":
            logging.info("OR")
            if topstack == "true" or beforetopstack == "true":
                result = "true"
            else:
                result = "false"
            asmfile.write(f""" // or {topstack} || {beforetopstack}
@{result}
D=A
@SP
A=M
M=D
@SP
M=M+1 // SP++
""")
        if operator == "gt":
            logging.info("GT")
            if topstack < beforetopstack:
                result == "true"
            else:
                result == "false"
            asmfile.write(f""" // greater than {topstack} < {beforetopstack}
@{result}
D=A
@SP
A=M
M=D
@SP
M=M+1 // SP++
""")
        if operator == "lt":
            logging.info("LT")
            if topstack > beforetopstack:
                result == "true"
            else:
                result == "false"
            asmfile.write(f""" // lower than {topstack} > {beforetopstack}
@{result}
D=A
@SP
A=M
M=D
@SP
M=M+1 // SP++
""")
        if operator == "and":
            logging.info("AND")
            if topstack == "true" and beforetopstack == "true":
                result == "true"
            else:
                result == "false"
            asmfile.write(f""" // and {topstack} & {beforetopstack}
@{result}
D=A
@SP
A=M
M=D
@SP
M=M+1 // SP++
""")
        if operator == "not":
            logging.info("NOT")
            if topstack == "true":
                result == "false"
            else:
                result == "true"
            asmfile.write(f""" // not {topstack}
@{result}
D=A
@SP
A=M
M=D
@SP
M=M+1 // SP++
""")