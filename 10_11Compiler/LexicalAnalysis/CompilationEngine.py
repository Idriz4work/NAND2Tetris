import re
import logging
import JackGrammar

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s -- %(message)s -- (%(asctime)s)')
# logging.basicConfig(level=logging.WARNING) to deactivate 

analysetable = JackGrammar.analyser_table

def startParsing(output_path, tokens, filename):
    compiler = CompilationEngine(output_path, filename)
    logging.critical("COMPILATION ENGINE STARTS")
    compiler.compile(tokens)


class CompilationEngine:
    def __init__(self, output_path, filename):
        self.filename = filename
        self.output_path = output_path
        self.file = open(output_path, 'w')
        
    def __del__(self):
        if hasattr(self, 'file'):
            self.file.close()

    def write(self, content):
        self.file.write(content)

    def compile(self, tokens):
        self.write(f"<{self.filename[:-4]}>\n")
        i = 0
        while i < len(tokens):
            i = self.compileSTATEMENT(tokens, i)
        self.write(f"</{self.filename[:-4]}>\n")

    def compileSTATEMENTS(self, tokens, i):
        logging.info("COMPILE STATEMENTS")
        while i < len(tokens):
            if tokens[i] in ["if", "while", "let", "do", "return"]:
                logging.info(f"Found token '{tokens[i]}' in STATEMENTS at index {i}")
                i = self.compileSTATEMENT(tokens, i)
            else:
                break
        return i

    def compileSTATEMENT(self, tokens, i):
        if i >= len(tokens):
            return i
        token = tokens[i]
        statement_types = {
            "while": self.compileWHILE,
            "if": self.compileIF,
            "return": self.compile_RETURN,
            "let": self.compileLetSTATEMENT,
            "do": self.compile_DO
        }
        if token in statement_types:
            return statement_types[token](tokens, i)
        elif token in analysetable.allSymbols:
            self.write(f"<symbol>{token}</symbol>\n")
            return i + 1
        elif token == "class":
            self.write(f"<class>{token}</class>\n")
            return i + 1
        else:
            # Handle other token types (identifiers, keywords, etc.)
            self.write(f"<token>{token}</token>\n")
            return i + 1

    def compileIF(self, tokens, i):
        logging.info(f"Compiling 'if' statement at index {i}")
        self.write("<ifStatement>\n")
        self.write("<keyword>if</keyword>\n")
        i += 1
        if tokens[i] == "(":
            self.write("<symbol>(</symbol>\n")
            i += 1
        i = self.compileEXPRESSION(tokens, i)
        if tokens[i] == ")":
            self.write("<symbol>)</symbol>\n")
            i += 1
        if tokens[i] == "{":
            self.write("<symbol>{</symbol>\n")
            i += 1
        i = self.compileSTATEMENTS(tokens, i)
        if tokens[i] == "}":
            self.write("<symbol>}</symbol>\n")
            i += 1
        # Handle 'else' part if present
        if i < len(tokens) and tokens[i] == "else":
            self.write("<keyword>else</keyword>\n")
            i += 1
            if tokens[i] == "{":
                self.write("<symbol>{</symbol>\n")
                i += 1
            i = self.compileSTATEMENTS(tokens, i)
            if tokens[i] == "}":
                self.write("<symbol>}</symbol>\n")
                i += 1
        self.write("</ifStatement>\n")
        return i

    def compileWHILE(self, tokens, i):
        logging.info(f"Compiling 'while' statement at index {i}")
        self.write("<whileStatement>\n")
        self.write("<keyword>while</keyword>\n")
        i += 1
        if tokens[i] == "(":
            self.write("<symbol>(</symbol>\n")
            i += 1
        i = self.compileEXPRESSION(tokens, i)
        if tokens[i] == ")":
            self.write("<symbol>)</symbol>\n")
            i += 1
        if tokens[i] == "{":
            self.write("<symbol>{</symbol>\n")
            i += 1
        i = self.compileSTATEMENTS(tokens, i)
        if tokens[i] == "}":
            self.write("<symbol>}</symbol>\n")
            i += 1
        self.write("</whileStatement>\n")
        return i

    def compileLetSTATEMENT(self, tokens, i):    
        logging.info(f"Compiling 'let' statement at index {i}")
        self.write("<letStatement>\n")
        self.write("<keyword>let</keyword>\n")
        i += 1  # Move past 'let'
        
        if i < len(tokens):
            self.write(f"<identifier>{tokens[i]}</identifier>\n")
            i += 1
        
        if tokens[i] == "[":
            self.write("<symbol>[</symbol>\n")
            i += 1
            i = self.compileEXPRESSION(tokens, i)
            if tokens[i] == "]":
                self.write("<symbol>]</symbol>\n")
                i += 1
        
        if tokens[i] == "=":
            self.write("<symbol>=</symbol>\n")
            i += 1
        
        i = self.compileEXPRESSION(tokens, i)
        
        if tokens[i] == ";":
            self.write("<symbol>;</symbol>\n")
            i += 1
        
        self.write("</letStatement>\n")
        return i

    def compile_DO(self, tokens, i):
        logging.info(f"Compiling 'do' statement at index {i}")
        self.write("<doStatement>\n")
        self.write("<keyword>do</keyword>\n")
        i += 1
        i = self.compile_SUBROUTINE_CALL(tokens, i)
        if tokens[i] == ";":
            self.write("<symbol>;</symbol>\n")
            i += 1
        self.write("</doStatement>\n")
        return i

    def compile_RETURN(self, tokens, i):
        logging.info(f"Compiling 'return' statement at index {i}")
        self.write("<returnStatement>\n")
        self.write("<keyword>return</keyword>\n")
        i += 1
        if tokens[i] != ";":
            i = self.compileEXPRESSION(tokens, i)
        if tokens[i] == ";":
            self.write("<symbol>;</symbol>\n")
            i += 1
        self.write("</returnStatement>\n")
        return i

    # The rest of the methods (compileEXPRESSION, compileTERM, etc.) remain the same
    # Just remember to remove any `if i < len(tokens):` checks at the beginning of these methods as well

    def compileEXPRESSION(self, tokens, i):
        logging.info(f"Compiling expression starting at index {i}")
        self.write("<expression>\n")
        i = self.compileTERM(tokens, i)
        while tokens[i] in analysetable.Operators:
            self.write(f"<symbol>{tokens[i]}</symbol>\n")
            i += 1
            i = self.compileTERM(tokens, i)
        self.write("</expression>\n")
        return i

    def compileTERM(self, tokens, i):
        logging.info(f"Compiling term starting at index {i}")
        self.write("<term>\n")
        if i < len(tokens):
            if tokens[i].isdigit():
                self.write(f"<integerConstant>{tokens[i]}</integerConstant>\n")
                i += 1
            elif tokens[i][0] == '"' and tokens[i][-1] == '"':
                self.write(f"<stringConstant>{tokens[i][1:-1]}</stringConstant>\n")
                i += 1
            elif self.is_string_constant(tokens[i],i):
                self.write(f"<keyword>{tokens[i]}</keyword>\n")
                i += 1
            elif tokens[i] == "(":
                self.write("<symbol>(</symbol>\n")
                i += 1
                i = self.compileEXPRESSION(tokens, i)
                if tokens[i] == ")":
                    self.write("<symbol>)</symbol>\n")
                    i += 1
            elif tokens[i] in analysetable.Operators:
                self.write(f"<symbol>{tokens[i]}</symbol>\n")
                i += 1
                i = self.compileTERM(tokens, i)
            else:
                # Assume it's an identifier
                self.write(f"<identifier>{tokens[i]}</identifier>\n")
                i += 1
                if tokens[i] == "[":
                    self.write("<symbol>[</symbol>\n")
                    i += 1
                    i = self.compileEXPRESSION(tokens, i)
                    if tokens[i] == "]":
                        self.write("<symbol>]</symbol>\n")
                        i += 1
                elif tokens[i] in ["(", "."]:
                    i = self.compile_SUBROUTINE_CALL(tokens, i - 1)
        self.write("</term>\n")
        return i

    def compile_SUBROUTINE_CALL(self, tokens, i):
        logging.info(f"Compiling subroutine call starting at index {i}")
        self.write(f"<identifier>{tokens[i]}</identifier>\n")
        i += 1
        if tokens[i] == ".":
            self.write("<symbol>.</symbol>\n")
            i += 1
            self.write(f"<identifier>{tokens[i]}</identifier>\n")
            i += 1
        if tokens[i] == "(":
            self.write("<symbol>(</symbol>\n")
            i += 1
            i = self.compile_EXPRESSION_LIST(tokens, i)
            if tokens[i] == ")":
                self.write("<symbol>)</symbol>\n")
                i += 1
        return i

    def compile_EXPRESSION_LIST(self, tokens, i):
        logging.info(f"Compiling expression list starting at index {i}")
        self.write("<expressionList>\n")
        if tokens[i] != ")":
            i = self.compileEXPRESSION(tokens, i)
            while tokens[i] == ",":
                self.write("<symbol>,</symbol>\n")
                i += 1
                i = self.compileEXPRESSION(tokens, i)
        self.write("</expressionList>\n")
        return i

    def is_integer_constant(self, token, i):
        if token.isdigit() and 0 <= int(token) <= 32767:
            self.write(f"<intconstant>{token}</intconstant>\n")
        else:
            return "not valid"
        return i

    def is_string_constant(self, token, i):
        if token.startswith('"') and token.endswith('"') and '\n' not in token:
            self.write(f"<stringconstant>{token}</stringconstant>\n")
        else:
            return "not valid"
        return i

    def is_identifier(self, token, i):
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', token) is not None:
            self.write(f"<identifier>{token}</identifier>\n")
        else:
            return "not valid"
        return i

    def advance(self, i):
        return i + 1