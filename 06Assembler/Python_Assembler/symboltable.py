# symboltable.py

class Dest:
    def __init__(self):
        self.codes = {
            "null": "000",
            "M":    "001",
            "D":    "010",
            "MD":   "011",
            "A":    "100",
            "AM":   "101",
            "AD":   "110",
            "AMD":  "111"
        }
    def get_char(self, code):
        for char, binary in self.codes.items():
            if code == char:
                return binary
        return "Not found"

class Jump:
    def __init__(self):
        self.codes = {
            "null": "000",
            "JGT":  "001",
            "JEQ":  "010",
            "JGE":  "011",
            "JLT":  "100",
            "JNE":  "101",
            "JLE":  "110",
            "JMP":  "111"
        }
    def get_char(self, code):
        for char, binary in self.codes.items():
            if code == char:
                return binary
        return "Not found"

class CompTable:
    def __init__(self):
        self.codes = {
            "0":      "101010",
            "1":      "111111",
            "-1":     "111010",
            "D":      "001100",
            "A":      "110000",
            "!D":     "001101",
            "!A":     "110001",
            "-D":     "001111",
            "-A":     "110011",
            "D+1":    "011111",
            "A+1":    "110111",
            "D-1":    "001110",
            "A-1":    "110010",
            "D+A":    "000010",
            "D-A":    "010011",
            "A-D":    "000111",
            "D&A":    "000000",
            "D|A":    "010101",
            "M":      "110000",
            "!M":     "110001",
            "-M":     "110011",
            "M+1":    "110111",
            "M-1":    "110010",
            "D+M":    "000010",
            "D-M":    "010011",
            "M-D":    "000111",
            "D&M":    "000000",
            "D|M":    "010101"
        }
    
    def get_char(self, code):
        for char, binary in self.codes.items():
            if code == char:
                return binary
        return "Not found"
