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

//push constant 17
@17
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++

//push constant 17
@17
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++
//eq
@SP
A=M
D=M
@END_JEQ
D=M;JEQ //if less than

//push constant 17
@17
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++

//push constant 16
@16
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++
//eq
@SP
A=M
D=M
@END_JEQ
D=M;JEQ //if less than

//push constant 16
@16
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++

//push constant 17
@17
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++
//eq
@SP
A=M
D=M
@END_JEQ
D=M;JEQ //if less than

//push constant 892
@892
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++

//push constant 891
@891
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++
 //lt
@SP
A=M
D=M
@END_JLT
D=M;JLT //if less than

//push constant 891
@891
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++

//push constant 892
@892
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++
 //lt
@SP
A=M
D=M
@END_JLT
D=M;JLT //if less than

//push constant 891
@891
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++

//push constant 891
@891
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++
 //lt
@SP
A=M
D=M
@END_JLT
D=M;JLT //if less than

//push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++

//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++
//gt
@SP
A=M
D=M
@END_JGT
D=M;JGT //if less than

//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++

//push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++
//gt
@SP
A=M
D=M
@END_JGT
D=M;JGT //if less than

//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++

//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++
//gt
@SP
A=M
D=M
@END_JGT
D=M;JGT //if less than

//push constant 57
@57
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++

//push constant 31
@31
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++

//push constant 53
@53
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

//push constant 112
@112
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

// negate
@SP
A=M-1
M=-M

// and
@SP
AM=M-1
D=M
A=A-1
M=M&D

//push constant 82
@82
D=A
@SP
A=M
M=D
@SP 
M=M+1 // SP++

// or
@SP
AM=M-1
D=M
A=A-1
M=M|D

// not
@SP
A=M-1
M=!M
//END OF FILE
