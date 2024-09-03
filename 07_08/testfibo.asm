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
@LCL
D=M
@init 0
A=D
    // nVARS
    @0
    D=A
    @0 // current number
    A=M
    M=D
    @LCL
    M=D
    