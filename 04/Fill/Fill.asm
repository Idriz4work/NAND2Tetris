// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the Keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// Replace this comment with your code.

@0
D=A
@counter
M=D

@SCREEN
D=A
@address
M=D

@KBD
D=A
@kboard
M=D

@BaseLoop
0;JMP

(BaseLoop)
@kboard
D=M
// if kdb is pressed go to filler
@Filler
D;JNE

// else it's 0 so clear screen
@SCREENCLEANER
D;JEQ

@BaseLoop
0;JMP

(Filler) // loop
@address
D=A
@counter
M=D+1
D=M

M=-1  // 16 black dots = -1

@counter
D=A+1

@BaseLoop
0;JMP

(SCREENCLEANER)
@address
D=A
@counter
M=D+1
D=M

M=0  // 16 black dots = -1

@counter
D=A+1

@BaseLoop
0;JMP

//(counterreset)
//@counter
//D=0
//M=D
//
//@BaseLoop
//0;JMP
