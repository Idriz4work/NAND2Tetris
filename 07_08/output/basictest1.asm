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

//push constant 10
@10
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++

//push constant 21
@21
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++

//push constant 22
@22
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++

//pop argument 2
@2
D=A
@ARG
D=M+D // D == 2 + 2 (4)
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

//pop argument 1
@1
D=A
@ARG
D=M+D // D == 2 + 1 (3)
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

//push constant 36
@36
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++

//pop this 6
@6
D=A
@THIS
D=M+D // addr=2+6 (8)
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

//push constant 42
@42
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++

//push constant 45
@45
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++

//pop that 5
@5
D=A
@THAT
D=M+D // D == 3 + 5 (8) 
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

//pop that 2
@2
D=A
@THAT
D=M+D // D == 3 + 2 (5) 
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

//push constant 510
@510
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++

//pop temp 6
@6
D=A
@11
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
@11 // store D at calculated address
A=M
M=D
@SP
A=M
M=D

//push that 5
@5
D=A
@THAT
A=M+D // *address = *sp A == 4 + 5 (9) 
D=M
@SP
A=M
M=D
@SP // SP++
M=M+1 // SP++

// add
@SP
AM=M-1
D=M
A=A-1
M=M+D

//push argument 1 
@1
D=A
@ARG
A=M+D // A == 2 + 1 (3) 
D=M
@SP
A=M
M=D
@SP
M=M+1 // SP++

// subtract
@SP
AM=M-1
D=M
A=A-1
M=M-D

//push this 6
@6
D=A
@THIS
A=M+D // A == 3 + 6 (9) 
D=M
@SP
A=M
M=D
@SP // SP++
M=M+1 // SP++

//push this 6
@6
D=A
@THIS
A=M+D // A == 3 + 6 (9) 
D=M
@SP
A=M
M=D
@SP // SP++
M=M+1 // SP++

// add
@SP
AM=M-1
D=M
A=A-1
M=M+D

// subtract
@SP
AM=M-1
D=M
A=A-1
M=M-D

//push temp 6
@6
D=A
@11
A=M
M=D
@SP
A=M
M=D
@SP
M=M+1 // SP++

// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
//END OF FILE
