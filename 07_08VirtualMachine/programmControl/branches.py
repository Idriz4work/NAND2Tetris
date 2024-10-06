import  re 
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s -- %(message)s -- (%(asctime)s)')

def writereturns(value, lastvalue, file_path):
    parts = value.split()
    functionname = parts[0]
    i = parts[-1]
    with open(file_path, 'a') as asmfile:
        asmfile.write(f""" // return {value}
  // endframe = LCL
  @LCL
  D=M
  @R13  // Use R13 as endframe
  M=D
  // retAddr = *(endframe - 5)
  @5
  A=D-A
  D=M
  @R14  // Use R14 to store return address
  M=D
  // *ARG = pop()
  @SP
  AM=M-1
  D=M
  @ARG
  A=M
  M=D
  // SP = ARG + 1
  @ARG
  D=M+1
  @SP
  M=D
  // Restore THAT
  @R13
  AM=M-1
  D=M
  @THAT
  M=D
  // Restore THIS
  @R13
  AM=M-1
  D=M
  @THIS
  M=D
  // Restore ARG
  @R13
  AM=M-1
  D=M
  @ARG
  M=D
  // Restore LCL
  @R13
  AM=M-1
  D=M
  @LCL
  M=D
  // goto retAddr
  @R14
  A=M
  @{functionname}
  0;JMP
""")

def writecalls(value,nARGS,file_path):
    parts = value.split()
    i = parts[-1]
    with open(file_path,'a') as asmfile:
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
@{nARGS}
D=A
// LCL = SP
@SP
D=A
@LCL
A=D
""")
        # goto {functionname}
        writegoto(parts[0],file_path=file_path)
        # insert labelname

"""
1. declare function (function)
2. nVARS * push 0 
3. nVARS - 1
4. if nVARS == 0 goto returnaddress
5. else goto function
"""
def writefunctions(value, nVARS,file_path):
    # Remove the keyword 'function' and trim whitespace
    value = value.replace('function', '').strip()
    
    # Split the remaining string on any digits (which will be the number)
    parts = re.split(r'\s*\d+', value)  # Splits by digits and optional surrounding whitespace
    
    # The first part will be the function name (e.g., 'sys.init')
    name = parts[0].strip()
    
    with open(file_path, 'a') as asmfile:
        i = 0
        asmfile.write(f"//function\n({name})\n")
        while i < int(nVARS):
            logging.info("push 0")
            asmfile.write(f""" // push 0
D=0
@SP
A=M
D=M
@SP
M=M+1 // SP++
""")
            i+=1
        writegoto(name,file_path=file_path)


def writeloops(value,file_path):
    parts = value.split()
    name = parts[1]
    with open(file_path,'a') as asmfile:
        asmfile.write(f"""
// LOOP
({name})
""")

def writegoto(value,file_path):
    parts = value.split()
    name = parts[0]
    with open(file_path,'a') as asmfile:
        asmfile.write(f"""
// goto 
goto {name}
D;JMP
""")

def writeifs(value, symbol, file_path):
    parts = value.split()
    name = parts[1]
    with open(file_path,'a') as asmfile:
        asmfile.write(f"""
// if-goto
@SP
AM=M-1
D=M
@{name}
D;{symbol}
""")
