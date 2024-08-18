// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

// r2 = result
@R2
D=0
M=D

// giving r0 the value of ram[0] 
@R0
D=M
@ISVALID
D;JEQ

// giving r1 the value of ram[1] 
@R1
D=M
@ISVALID
D;JEQ

@MULTIPLICATION
D;JEQ

(MULTIPLICATION)

// D gets value of number1
@R0
D=M
M=D

// R2 is the result of num1 + num1
@R2
M=D+M

// subtracting 1 
@R1
D=M-1
M=D
@END
D;JEQ

// loop again
@MULTIPLICATION
0;JMP

// checking if ram1 / ram2 is 0 from beginning
(ISVALID)
@R2
M=0
@END
D;JMP

// terminating the code for security reason
(END)
@END
0;JMP