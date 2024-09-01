import config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s -- %(message)s -- (%(asctime)s)')

# J keeps track of the address we are in static
j = 0


""" POP LOGIC
a) Calculate the target address
b) Store it in a temporary location (R13)
c) Decrement SP and get the top stack value
d) Store that value at the calculated address
"""

def poper(statement, symbol):
    parts = statement.split()
    i = int(parts[2])
    outputfileforstatic = config.outputfile[0:-5]
    with open(config.outputfile, 'a') as asmfile:
        asmfile.write(f"\n//{statement}")
        if symbol.name == "local":
            asmfile.write(f"""
@{i}
D=A
@LCL
D=M+D // D=LCL(1)+{i} == {1+i}
@R13 // general purpose register
M=D
@SP
AM=M-1
D=M
@R13
A=M
D=M
@LCL // store D at calculated address
A=M
M=D
@SP
A=M
M=D
""")
        elif symbol.name == "static":
            asmfile.write(f"""@16 // access address
D=A
@{outputfileforstatic}.{i} 
M=D // store 16 in M 
@{j}
D=M
@{outputfileforstatic}.{i}
A=M+D // add 16 + {j} to M
D=M
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@{outputfileforstatic}.{i}
A=M
M=D
@SP
A=M
M=D
""")
            j+=1
        elif symbol.name == "argument":
            asmfile.write(f"""
@{i}
D=A
@ARG
D=M+D // D == 2 + {i} ({2+i})
@R13 // general purpose register
M=D
@SP
AM=M-1
D=M
@R13 // general purpose register
A=M
M=D
@ARG // store D at calculated address
A=M
M=D
@SP
A=M
M=D
""")
        elif symbol.name == "this":
            asmfile.write(f"""
@{i}
D=A
@THIS
D=M+D // addr=2+{i} ({2+i})
@R13 // general purpose register
M=D
@SP
AM=M-1
D=M
@R13 // general purpose register
A=M
M=D
@THIS // store D at calculated address
A=M
M=D
@SP
A=M
M=D
""")
        elif symbol.name == "that":
            asmfile.write(f"""
@{i}
D=A
@THAT
D=M+D // D == 3 + {i} ({3+i}) 
@R13 // general purpose register
M=D
@SP
AM=M-1 //  SP-- Address(A) & value(M) A-- & M--
D=M
@R13 // general purpose register
A=M
M=D
@THAT // store D at calculated address
A=M
M=D
@SP
A=M
M=D
""")
        elif symbol.name == "temp":
            asmfile.write(f"""
@{i}
D=A
@{5 + i}
A=M
M=D
@R13 // general purpose register
M=D
@SP
AM=M-1 //  SP-- Address(A) & value(M) A-- & M--
D=M
@R13 // general purpose register
A=M
M=D
@{5+i} // store D at calculated address
A=M
M=D
@SP
A=M
M=D
""")
        elif symbol.name == "pointer0":
            asmfile.write(f"""@SP
AM=M-1
D=M
@THIS
M=D
""")
        elif symbol.name == "pointer1":
            asmfile.write(f"""@SP
AM=M-1
D=M
@THAT
M=D
""")

""" PUSH LOGIC
a) calculate target address
b) set address to value
c) increment SP
"""
def pusher(statement, symbol):
    parts = statement.split()
    i = int(parts[2])
    outputfileforstatic = config.outputfile[0:-5]
    with open(config.outputfile, 'a') as asmfile:
        asmfile.write(f"\n//{statement}")
        if symbol.name == "constant":
            asmfile.write(f"""
@{i}
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++
""")
        elif symbol.name == "local":
            asmfile.write(f"""
@{i}
D=A
@LCL
A=M+D // A == 1 + {i} ({1+i}) 
D=M
@SP
A=M
M=D
@SP 
M=M+1 // SP++
""")
        elif symbol.name == "static":
            asmfile.write(f"""@16 // access address
D=A
@{outputfileforstatic}.{i} // access value
M=D // store 16 in M 
@{j}
D=M
@{outputfileforstatic}.{i}
A=M+D // add 16 + {j} to M
D=M
@SP
A=M
M=D
@SP 
M=M+1 // SP++
""")
        elif symbol.name == "argument":
            asmfile.write(f""" 
@{i}
D=A
@ARG
A=M+D // A == 2 + {i} ({2+i}) 
D=M
@SP
A=M
M=D
@SP
M=M+1 // SP++
""")
        elif symbol.name == "this":
            asmfile.write(f"""
@{i}
D=A
@THIS
A=M+D // A == 3 + {i} ({3+i}) 
D=M
@SP
A=M
M=D
@SP // SP++
M=M+1 // SP++
""")
        elif symbol.name == "that":
            asmfile.write(f"""
@{i}
D=A
@THAT
A=M+D // *address = *sp A == 4 + {i} ({4+i}) 
D=M
@SP
A=M
M=D
@SP // SP++
M=M+1 // SP++
""")
        elif symbol.name == "temp":

            asmfile.write(f"""
@{i}
D=A
@{5 + i}
A=M
M=D
@SP
A=M
M=D
@SP
M=M+1 // SP++
""")
        elif symbol.name == "pointer0":
            asmfile.write(f"""@SP
A=M
D=M
@THIS
M=D
@SP
M=M+1
""")
        elif symbol.name == "pointer1":
            asmfile.write(f"""@SP
A=M
D=M
@THIS
M=D
@SP
M=M+1
""")
