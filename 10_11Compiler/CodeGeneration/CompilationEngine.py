import CodeGeneration.symboltable as SY
import os
import re
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO, format=' - %(levelname)s - %(message)s -- [%(filename)s:%(lineno)d]')

def startCompiling(values: List[str], output_path: str, filename: str):
    
    logging.critical("Starts the compilation process.")
    
    compiler = CompilationEngine(output_path, filename)
    logging.info("COMPILATION ENGINE STARTS VM CODE")
    compiler.compile(values)

class CompilationEngine:
    def __init__(self, output_path, filename):
        self.filename = filename
        self.output_path = output_path
        self.class_table = SY.SymbolTables.SymbolTableClass()
        self.subroutine_table = SY.SymbolTables.SymbolTableSubroutine()
        self.file = None

    def compile(self, values: List[str]):
        """
        Main compilation method that processes the input values.
        """
        logging.info("Starting compilation")
        try:
            with open(self.output_path, 'a') as self.file:
                i = 0
                while i < len(values):
                    value = values[i]
                    vls = self.class_table.getValues(value)
                    if vls == "not found":
                        vls = self.subroutine_table.getValues(value)
                    if vls == "not found":
                        logging.warning(f"Value not found in symbol tables: {value}")
                        i += 1
                        continue
                    if vls == None:
                        i+=1
                        continue

                    name, ty, kind, num = vls['NAME'], vls['TYPE'], vls['KIND'], vls['NUMBER']
                    logging.info(f"CURRENNT VALUE: {value}")
                    i = self.process_identifier(values=values,name=name, ty=ty, kind=kind, num=num, i=i)
            logging.info("Compilation completed")
        except Exception as e:
            logging.info(f"{e}")

    def write(self, value):
        """
        Writes a value to the output file.
        """
        self.file.write(value + '\n')


    def process_identifier(self,values, name,ty,kind,i,num):
        """
        Processes an identifier based on its kind.
        """
        logging.info("process identifier")
        if kind in ["var", "argument", "static"]:
            return self.is_identifierVAS(name, ty, num, i)
        elif kind == "field":
            return self.is_identifierFIELD(values,name, ty, num, i)
        elif kind == "class":
            return self.is_identifierCLASS(values=values,name=name,ty=ty,num=num, i=i)
        elif kind == "subroutine":
            return self.is_identifierSUBROUTINE(name, i)
        else:
            logging.warning(f"Unknown identifier kind: {kind}")
            return self.advance(i)

    def is_identifierVAS(self, name,ty,num,i):
        """
        Handles var, argument, and static identifiers.
        """
        logging.info("VAS IDENT")
        self.write(f"push {ty} {num}")
        return self.advance(i)

    def is_identifierFIELD(self,values, name,ty,num,i):
        logging.info("""Handles field identifiers.""")
        self.write(f"push this {num}")
        return self.advance(i)

    def is_identifierCLASS(self,values, name,ty,num, i):
        logging.info("""Handles class identifiers.""")
        self.write(f"function {name}.{name} {num}")
        self.compileSTATEMENTS(values=values,i=i)
        # Add logic for class compilation
        return self.advance(i)

    def is_identifierSUBROUTINE(self, name, i):
        logging.info("""Handles subroutine identifiers.""")

        self.write(f"")
        self.subroutine_table.reset(name)
        # Add logic for subroutine compilation
        return self.advance(i)

    def compileOperation(self, value,i,is_unary):
        logging.info("""Compiles arithmetic and unary operations.""")
        arithmetic_ops = {
            "+": "add",
            "-": "sub",
            "*": "call Math.multiply 2",
            "/": "call Math.divide 2",
            "&": "and",
            "|": "or",
            "<": "lt",
            ">": "gt",
            "=": "eq"
        }
        unary_ops = {
            "-": "neg",
            "~": "not"
        }
        
        ops = unary_ops if is_unary else arithmetic_ops
        if value in ops:
            self.write(ops[value])
        else:
            op_type = "unary" if is_unary else "arithmetic"
            logging.warning(f"Unknown {op_type} operation: {value}")
        return self.advance(i)

    def compileSTATEMENTS(self, values,i):
        logging.info("""Compiles a series of statements.""")
        while i < len(values) and values[i] != '}':
            i = self.compileSTATEMENT(values, i)
        return self.advance(i)

    def compileSTATEMENT(self, values,i):
        logging.info(f"""Compiles a single statement: {values[i]}""")
        if values[i] == 'if':
            return self.compileIF(values, i)
        elif values[i] == 'while':
            return self.compileWHILE(values, i)
        elif values[i] == 'let':
            return self.compileLetSTATEMENT(values, i)
        elif values[i] == 'do':
            return self.compile_DO(values, i)
        elif values[i] == 'return':
            return self.compile_RETURN(values, i)
        else:
            return self.advance(i)
            #logging.warning(f"Unknown statement type: {values[i]}")

    def compileIF(self, values, i):
        logging.info("Compiles a if statement.")
        """
        Compiles an if statement.
        """
        # Implementation for if statement
        row = SY.SymbolTables.SymbolTableSubroutine.getValues(values[i])
        name = row[0]
        row = SY.SymbolTables.SymbolTableSubroutine.getValues(values[i+1])
        op = row[0]
        row = SY.SymbolTables.SymbolTableClass.getValues(values[i])
        num = row
        self.write(f"if-goto {name}_{op}_{num}\n")
        self.write(f"label {name}_{op}_{num}\n")
        # self.write(f"goto")
        return self.advance(i)

    def compileWHILE(self, values,i):
        logging.info("Compiles a while statement.")
        """
        Compiles a while statement.
        """
        # Implementation for while statement
        num = 1
        nameofloop = f"LOOP{num}"
        num+=1
        self.write(f"label {nameofloop}\n")
        i+1
        if values[i] == '(':
            i = self.compileEXPRESSION(values,i+1)
        if values[i] == ')':
            i+1
        if values[i] == '{':
            i+=1
            i = self.compileSTATEMENTS(values,i)
        if values[i+1] == '}':
            self.write(f"goto {nameofloop}")
            i+=1
        return self.advance(i)

    def compileLetSTATEMENT(self, values,i):
        logging.info("Compiles a let statement.")
        """
        Compiles a let statement.
        """
        # Implementation for let statement
        return self.advance(i)

    def compile_DO(self, values,i):
        logging.info("Compiles a do statement.")
        """
        Compiles a do statement.
        """
        # Implementation for do statement
        return self.advance(i)

    def compile_RETURN(self, values,i):
        logging.info("Compiles a return statement.")
        """
        Compiles a return statement.
        """
        # Implementation for return statement
        return self.advance(i)

    def codewrite(self,values,i):
        logging.info("Compile code write.")
        if self.is_integer_constant(values[i]) != 'not valid':
            self.write(f"push {values[i]}")
            return self.advance(i)
        if self.is_identifierVAS(values[i],i=i) != 'not valid':
            self.write(f"push {values[i]}")
            return self.advance(i)
        if self.compile_EXPRESSION_LIST(values[i],i) != 'not valid' and self.compileOperation(values[i],i+1) != 'not valid' and self.compileEXPRESSION(values[i],i+2) != "not valid":
            self.codewrite(values,i)
            self.codewrite(values,i+2)
            return self.advance(i)
        if self.compileOperation(values[i],i) != 'not valid' and self.compileEXPRESSION(values[i+1],i+1) != 'not valid':
            self.codewrite(values[i+1],i+1) # expression
            self.write(f"{values[i]}") # operation
            return self.advance(i)
        if self.compile_EXPRESSION_LIST(values,i):
            self.codewrite(values[i],i) # 1. expression
            self.codewrite(values[i],i+1) # 2. expression
            # more expressions...
            return self.advance(i)
        return self.advance(i)

    def compileEXPRESSION(self, values,i):
        logging.info("Compiles a expression statement.")
        """
        Compiles an expression.
        """
        # Implementation for expression compilation
        return self.advance(i)

    def compileTERM(self, values,i):
        logging.info("Compiles a term statement.")
        """
        Compiles a term.
        """
        # Implementation for term compilation
        return self.advance(i)

    def compile_SUBROUTINE_CALL(self, values,i):
        logging.info("Compiles a subroutine statement.")
        """
        Compiles a subroutine call.
        """
        # Implementation for subroutine call compilation
        return self.advance(i)

    def compile_EXPRESSION_LIST(self, values,i):
        logging.info("Compiles a EXP LIST statement.")
        """
        Compiles an expression list.
        """
        # Implementation for expression list compilation
        return self.advance(i)

    def is_integer_constant(self, value):
        """
        Checks if a value is an integer constant.
        """
        try:
            int_value = int(value)
            return 0 <= int_value <= 32767  # 16-bit integer range
        except ValueError:
            return False

    def is_string_constant(self, value):
        """
        Checks if a value is a string constant.
        """
        return value.startswith('"') and value.endswith('"')

    def advance(self, i: int) -> int:
        """
        Advances the token index.
        """
        return i + 1

