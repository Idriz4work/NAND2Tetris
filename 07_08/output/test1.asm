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

//push argument 1         // sets THAT, the base address of the 
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

//push constant 0         // sets the series' first and second
@0
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++

//pop that 0              // elements to 0 and 1, respectively
@0
D=A
@THAT
D=M+D // D == 3 + 0 (3) 
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

//push constant 1
@1
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++

//pop that 1
@1
D=A
@THAT
D=M+D // D == 3 + 1 (4) 
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

//push argument 0         // sets n, the number of remaining elements 
@0
D=A
@ARG
A=M+D // A == 2 + 0 (2) 
D=M
@SP
A=M
M=D
@SP
M=M+1 // SP++

//push constant 2         // to be computed, to argument[0] minus 2,
@2
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++

//pop argument 0
@0
D=A
@ARG
D=M+D // D == 2 + 0 (2)
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

// LOOP
(LOOP)

//push argument 0 
@0
D=A
@ARG
A=M+D // A == 2 + 0 (2) 
D=M
@SP
A=M
M=D
@SP
M=M+1 // SP++

// if statement
@COMPUTE_ELEMENT
D;JMP

// goto 
@END
D;JMP

// LOOP
(COMPUTE_ELEMENT)

//push that 0
@0
D=A
@THAT
A=M+D // *address = *sp A == 4 + 0 (4) 
D=M
@SP
A=M
M=D
@SP // SP++
M=M+1 // SP++

//push that 1
@1
D=A
@THAT
A=M+D // *address = *sp A == 4 + 1 (5) 
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

//push constant 1
@1
D=A
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

//push argument 0 
@0
D=A
@ARG
A=M+D // A == 2 + 0 (2) 
D=M
@SP
A=M
M=D
@SP
M=M+1 // SP++

//push constant 1
@1
D=A
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

//pop argument 0
@0
D=A
@ARG
D=M+D // D == 2 + 0 (2)
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

// goto 
@LOOP
D;JMP

// LOOP
(END)
//END OF FILE
