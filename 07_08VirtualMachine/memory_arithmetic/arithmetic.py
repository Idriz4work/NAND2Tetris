import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s -- %(message)s -- (%(asctime)s)')

def ArithmeticOperations(topstack,beforetopstack,operator,file_path):
    logging.critical("starting arithmetic operations")
    with open(file_path,"a") as asmfile:
        if operator == "add":
            logging.info("ADD")
            asmfile.write(f"""
// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
""")
            
        if operator == "sub":
            logging.info("SUB")
            result = topstack - beforetopstack 
            asmfile.write(f"""
// subtract
@SP
AM=M-1
D=M
A=A-1
M=M-D
""")
        if operator == "neg":
            logging.info("NEG")
            asmfile.write(f"""
// negate
@SP
A=M-1
M=-M
""")
        possib = ["JGT","JEQ","JGE","JLT","JNE","JLE"]
        if operator == "eq":
            logging.info("EQ")
            asmfile.write(f"""//{operator}
@SP
A=M
D=M
@END_{possib[1]}
D=M;{possib[1]} //if less than
""")

        if operator == "gt":
            logging.info("GT")
            asmfile.write(f"""//{operator}
@SP
A=M
D=M
@END_{possib[0]}
D=M;{possib[0]} //if less than
""")
        if operator == "lt":
            logging.info("LT")
            asmfile.write(f""" //{operator}
@SP
A=M
D=M
@END_{possib[3]}
D=M;{possib[3]} //if less than
""")
        elif operator in ["and", "or"]:
            logging.info(operator.upper())
            op = "&" if operator == "and" else "|"
            asmfile.write(f"""
// {operator}
@SP
AM=M-1
D=M
A=A-1
M=M{op}D
""")
        if operator == "not":
            logging.info("NOT")
            asmfile.write(f"""
// not
@SP
A=M-1
M=!M
""")