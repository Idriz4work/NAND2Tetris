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

class SymbolTable:
    def __init__(self):
        self.symbols = {
            "R0":     "0",
            "R1":     "1",
            "R2":     "2",
            "R3":     "3",
            "R4":     "4",
            "R5":     "5",
            "R6":     "6",
            "R7":     "7",
            "R8":     "8",
            "R9":     "9",
            "R10":    "10",
            "R11":    "11",
            "R12":    "12",
            "R13":    "13",
            "R14":    "14",
            "R15":    "15",
            "SCREEN": "16384",
            "KBD":    "24576",
            "SP":     "0",
            "LCL":    "1",
            "ARG":    "2",
            "THIS":   "3",
            "THAT":   "4"
        }
    def add_symbol(self, name, address):
        if name not in self.symbols:
            self.symbols[name] = str(address)
        else:
            print(f"Warning: Symbol '{name}' already exists. Not overwriting.")

    def get_char(self, code):
        return self.symbols.get(code,None)

    def contains(self, name):
        return name in self.symbols

class Symbol:
    def __init__(self, name, address, digit, isA, isC):
        self.name = name        # string 
        self.address = address
        self.digit = digit          # integer
        self.isA = isA          # integer (usually treated as boolean in Python)
        self.isC = isC          # integer (usually treated as boolean in Python)

class variabless:
    def __init__(self, name, address, digit, variables):
        self.name = name        # string 
        self.address = address
        self.digit = digit          # integer
        self.variables = variables

class loops:
    def __init__(self, name, address, digit, loop):
        self.name = name        # string 
        self.address = address
        self.digit = digit          # integer
        self.loop = loop        # character
