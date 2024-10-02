import CodeGeneration.symboltable as SY
import LexicalAnalysis.JackGrammar as jg
import csv
import logging
from typing import List

analysetable = jg.analyser_table

logging.basicConfig(level=logging.INFO, format=' - %(levelname)s - %(message)s -- [%(filename)s:%(lineno)d]')

class CompilationEngine:
    def __init__(self, output_path, filename):
        self.filename = filename
        self.output_path = output_path
        self.class_table = self.load_csv('tableDATA/dataclass.csv')
        self.subroutine_table = self.load_csv('tableDATA/datasubroutine.csv')
        self.file = None
        self.label_counter = 0

    def load_csv(self, csv_filename):
        table = {}
        with open(csv_filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                table[row['NAME']] = row
        return table

    def compile(self,typename,values):
        logging.info("Starting compilation")
        try:
            value = typename
            with open(self.output_path, 'a') as self.file:
                i = 0
                vls = self.class_table.get(value) or self.subroutine_table.get(value)
                if not vls:
                    logging.warning(f"Value not found in symbol tables: {value}")
                    i += 1
                    return i
                name, ty, kind, num = vls['NAME'], vls['TYPE'], vls['KIND'], vls['NUMBER']
                logging.info(f"CURRENT VALUE: {value}")
                i = self.process_identifier(values, name, ty, kind, num, i)
            logging.info("Compilation completed")
        except Exception as e:
            logging.error(f"Compilation error: {e}")

    def process_identifier(self, values, name, ty, kind, num, i):
        logging.info("Processing identifier")
        if kind in ["var", "argument", "static", "field"]:
            return self.handle_variable(name, ty, kind, num, i)
        elif kind == "class":
            return self.handle_class(name, ty, num, i)
        elif kind == "subroutine":
            return self.handle_subroutine(name, ty, num, i)
        else:
            logging.warning(f"Unknown identifier kind: {kind}")
            return self.advance(i)

    def handle_variable(self, name, ty, kind, num, i):
        segment = kind if kind != "field" else "this"
        self.write(f"push {segment} {num}")
        return self.advance(i)

    def handle_class(self, name, ty, num, i):
        self.write(f"function {name}.{name} {num}")
        SY.SymbolTables.SymbolTableClass.reset()
        return self.compileSTATEMENTS(i)

    def handle_subroutine(self, name, ty, num, i):
        self.write(f"call {name}.{self.values[self.advance(i)]} {num}")
        SY.SymbolTables.SymbolTableSubroutine.reset()
        return self.advance(i)

    def compileSTATEMENTS(self, i):
        while i < len(self.values) and self.values[i] != '}':
            i = self.compileSTATEMENT(i)
        return self.advance(i)

    def compileSTATEMENT(self, i):
        if self.values[i] == 'if':
            return self.compileIF(i)
        elif self.values[i] == 'while':
            return self.compileWHILE(i)
        elif self.values[i] == 'let':
            return self.compileLetSTATEMENT(i)
        elif self.values[i] == 'do':
            return self.compile_DO(i)
        elif self.values[i] == 'return':
            return self.compile_RETURN(i)
        else:
            return self.advance(i)

    def compileIF(self, i):
        self.label_counter += 1
        label_true = f"IF_TRUE{self.label_counter}"
        label_false = f"IF_FALSE{self.label_counter}"
        label_end = f"IF_END{self.label_counter}"

        i = self.compileEXPRESSION(i + 2)  # Skip 'if' and '('
        self.write(f"not")
        self.write(f"if-goto {label_false}")
        
        i = self.compileSTATEMENTS(i + 2)  # Skip ')' and '{'
        self.write(f"goto {label_end}")
        self.write(f"label {label_false}")
        
        if self.values[i] == 'else':
            i = self.compileSTATEMENTS(i + 2)  # Skip 'else' and '{'
        
        self.write(f"label {label_end}")
        return i

    def compileWHILE(self, i):
        self.label_counter += 1
        label_exp = f"WHILE_EXP{self.label_counter}"
        label_end = f"WHILE_END{self.label_counter}"

        self.write(f"label {label_exp}")
        i = self.compileEXPRESSION(i + 2)  # Skip 'while' and '('
        self.write("not")
        self.write(f"if-goto {label_end}")
        
        i = self.compileSTATEMENTS(i + 2)  # Skip ')' and '{'
        self.write(f"goto {label_exp}")
        self.write(f"label {label_end}")
        return i

    def compileLetSTATEMENT(self, i):
        var_name = self.values[i + 1]
        var_info = self.class_table.get(var_name) or self.subroutine_table.get(var_name)
        
        if not var_info:
            logging.error(f"Variable {var_name} not found in symbol tables")
            return self.advance(i)

        i = self.compileEXPRESSION(i + 3)  # Skip 'let', var_name, and '='
        self.write(f"pop {var_info['KIND']} {var_info['NUMBER']}")
        return self.advance(i)  # Skip ';'

    def compile_DO(self, i):
        i = self.compile_SUBROUTINE_CALL(i + 1)  # Skip 'do'
        self.write("pop temp 0")  # Discard the return value
        return self.advance(i)  # Skip ';'

    def compile_RETURN(self, i):
        if self.values[i + 1] != ';':
            i = self.compileEXPRESSION(i + 1)
        else:
            self.write("push constant 0")
        self.write("return")
        return self.advance(i)  # Skip ';'

    def compileEXPRESSION(self, i):
        i = self.compileTERM(i)
        while self.values[i] in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            op = self.values[i]
            i = self.compileTERM(i + 1)
            if op == '+':
                self.write("add")
            elif op == '-':
                self.write("sub")
            elif op == '*':
                self.write("call Math.multiply 2")
            elif op == '/':
                self.write("call Math.divide 2")
            elif op == '&':
                self.write("and")
            elif op == '|':
                self.write("or")
            elif op == '<':
                self.write("lt")
            elif op == '>':
                self.write("gt")
            elif op == '=':
                self.write("eq")
        return i

    def compileTERM(self, i):
        if self.values[i].isdigit():
            self.write(f"push constant {self.values[i]}")
            return self.advance(i)
        elif self.values[i][0] == '"':
            string = self.values[i][1:-1]
            self.write(f"push constant {len(string)}")
            self.write("call String.new 1")
            for char in string:
                self.write(f"push constant {ord(char)}")
                self.write("call String.appendChar 2")
            return self.advance(i)
        elif self.values[i] in self.class_table or self.values[i] in self.subroutine_table:
            return self.handle_variable(self.values[i], None, None, None, i)
        elif self.values[i] == '(':
            i = self.compileEXPRESSION(i + 1)
            return self.advance(i)  # Skip ')'
        elif self.values[i] in ['-', '~']:
            op = self.values[i]
            i = self.compileTERM(i + 1)
            self.write("neg" if op == '-' else "not")
            return i
        else:
            return self.compile_SUBROUTINE_CALL(i)

    def compile_SUBROUTINE_CALL(self, i):
        name = self.values[i]
        if self.values[i + 1] == '.':
            name += f".{self.values[i + 2]}"
            i += 2
        
        i = self.compile_EXPRESSION_LIST(i + 2)  # Skip '('
        num_args = self.label_counter
        self.write(f"call {name} {num_args}")
        return self.advance(i)  # Skip ')'

    def compile_EXPRESSION_LIST(self, i):
        self.label_counter = 0
        while self.values[i] != ')':
            i = self.compileEXPRESSION(i)
            self.label_counter += 1
            if self.values[i] == ',':
                i += 1
        return i

    def write(self, value):
        self.file.write(value + '\n')

    def advance(self, i):
        return i + 1