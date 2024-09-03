// Initialize the stack pointer
@256
D=A
@SP
M=D

// Initialize other segments if needed for function calls
@860
D=A
@LCL
M=D
@400
D=A
@ARG
M=D
@2000
D=A
@THIS
M=D
@3000
D=A
@THAT
M=D                    
// [END OF PREPARATION]
//function init 0
@init 0
// nVARS
@0
D=A
@LCL
M=D

//push constant 4
@4
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++
 // push return address call Main.fibonacci 1
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
@call Main.fibonacci 1
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

// LOOP
(END)

// goto 
@goto END  // loops infinitely
D;JMP
//END OF FILE
