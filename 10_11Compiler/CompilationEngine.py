import re
import logging
import JackGrammar

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s -- %(message)s -- (%(asctime)s)')

analysetable = JackGrammar.analyser_table

# LL 1 Parser 
def startParsing(output_path, tokens, filename):
    compiler = CompilationEngine(output_path, filename)
    logging.critical("COMPILATION ENGINE STARTS")
    with open(output_path, 'w') as file:
        file.write(f"<{filename[:-4]}>\n")
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == "while":
                file.write("<whileStatement>\n")
                i = compiler.compileWHILE(tokens, i)
                file.write("</whileStatement>\n")
            elif token == "if":
                file.write("<ifStatement>\n")
                i = compiler.compileIF(tokens, i)
                file.write("</ifStatement>\n")
            elif token == "return":
                file.write("<returnStatement>\n")
                file.write("<keyword>return</keyword>\n")
                i += 1
                i = compiler.compile_RETURN(tokens, i)
                file.write("</returnStatement>\n")
            elif token in analysetable.allSymbols:
                file.write(f"<symbol>{token}</symbol>\n")
                i += 1
            elif token == "class":
                file.write(f"<class>{token}</class>\n")
                i += 1
            elif token == "let":
                file.write("<letStatement>\n")
                i = compiler.compileLetSTATEMENT(tokens, i)
                file.write("</letStatement>\n")
            elif token == "do":
                file.write("<doStatement>\n")
                i = compiler.compile_DO(tokens, i)
                file.write("</doStatement>\n")
            else:
                i += 1
        file.write(f"</{filename[:-4]}>\n")

class CompilationEngine:
    def __init__(self, output_path, filename):
        self.filename = filename
        self.output_path = output_path

    def compileSTATEMENTS(self, tokens, i):
        while i < len(tokens):
            if tokens[i] in ["if", "while", "let", "do", "return"]:
                i = self.compileSTATEMENT(tokens, i)
            else:
                break
        return i

    def compileSTATEMENT(self, tokens, i):
        if tokens[i] == "if":
            return self.compileIF(tokens, i)
        elif tokens[i] == "while":
            return self.compileWHILE(tokens, i)
        elif tokens[i] == "let":
            return self.compileLetSTATEMENT(tokens, i)
        elif tokens[i] == "do":
            return self.compile_DO(tokens, i)
        elif tokens[i] == "return":
            with open(self.filename,'a') as file:
                file.write("<keyword>return</keyword>\n")
                i += 1
            return self.compile_RETURN(tokens, i)
        return i + 1  # Skip unknown tokens

    def compileIF(self, tokens, i):
        with open(self.filename, 'a') as xmlfile:
            xmlfile.write("<keyword>if</keyword>\n")
            i += 1
            if i < len(tokens) and tokens[i] == "(":
                xmlfile.write("<symbol>(</symbol>\n")
                i += 1
            i = self.compileEXPRESSION(tokens, i)
            if i < len(tokens) and tokens[i] == ")":
                xmlfile.write("<symbol>)</symbol>\n")
                i += 1
            if i < len(tokens) and tokens[i] == "{":
                xmlfile.write("<symbol>{</symbol>\n")
                i += 1
            i = self.compileSTATEMENTS(tokens, i)
            if i < len(tokens) and tokens[i] == "}":
                xmlfile.write("<symbol>}</symbol>\n")
                i += 1
            # Handle 'else' part if present
            if i < len(tokens) and tokens[i] == "else":
                xmlfile.write("<keyword>else</keyword>\n")
                i += 1
                if i < len(tokens) and tokens[i] == "{":
                    xmlfile.write("<symbol>{</symbol>\n")
                    i += 1
                i = self.compileSTATEMENTS(tokens, i)
                if i < len(tokens) and tokens[i] == "}":
                    xmlfile.write("<symbol>}</symbol>\n")
                    i += 1
        return i

    def compileWHILE(self, tokens, i):
        with open(self.filename, 'a') as xmlfile:
            xmlfile.write("<keyword>while</keyword>\n")
            i += 1
            if i < len(tokens) and tokens[i] == "(":
                xmlfile.write("<symbol>(</symbol>\n")
                i += 1
            i = self.compileEXPRESSION(tokens, i)
            if i < len(tokens) and tokens[i] == ")":
                xmlfile.write("<symbol>)</symbol>\n")
                i += 1
            if i < len(tokens) and tokens[i] == "{":
                xmlfile.write("<symbol>{</symbol>\n")
                i += 1
            i = self.compileSTATEMENTS(tokens, i)
            if i < len(tokens) and tokens[i] == "}":
                xmlfile.write("<symbol>}</symbol>\n")
                i += 1
        return i

    def compileLetSTATEMENT(self, tokens, i):
        with open(self.filename, 'a') as xmlfile:
            xmlfile.write("<keyword>let</keyword>\n")
            i += 1
            if i < len(tokens):
                xmlfile.write(f"<identifier>{tokens[i]}</identifier>\n")
                i += 1
            if i < len(tokens) and tokens[i] == "[":
                xmlfile.write("<symbol>[</symbol>\n")
                i += 1
                i = self.compileEXPRESSION(tokens, i)
                if i < len(tokens) and tokens[i] == "]":
                    xmlfile.write("<symbol>]</symbol>\n")
                    i += 1
            if i < len(tokens) and tokens[i] == "=":
                xmlfile.write("<symbol>=</symbol>\n")
                i += 1
            i = self.compileEXPRESSION(tokens, i)
            if i < len(tokens) and tokens[i] == ";":
                xmlfile.write("<symbol>;</symbol>\n")
                i += 1
        return i

    def compile_DO(self, tokens, i):
        with open(self.filename, 'a') as xmlfile:
            xmlfile.write("<keyword>do</keyword>\n")
            i += 1
            i = self.compile_SUBROUTINE_CALL(tokens, i)
            if i < len(tokens) and tokens[i] == ";":
                xmlfile.write("<symbol>;</symbol>\n")
                i += 1
        return i

    def compile_RETURN(self, tokens, i):
        with open(self.filename, 'a') as xmlfile:
            if i < len(tokens) and tokens[i] != ";":
                i = self.compileEXPRESSION(tokens, i)
            if i < len(tokens) and tokens[i] == ";":
                xmlfile.write("<symbol>;</symbol>\n")
                i += 1
        return i

    def compileEXPRESSION(self, tokens, i):
        with open(self.filename, 'a') as xmlfile:
            xmlfile.write("<expression>\n")
            i = self.compileTERM(tokens, i)
            while i < len(tokens) and tokens[i] in analysetable.Operators:
                xmlfile.write(f"<symbol>{tokens[i]}</symbol>\n")
                i += 1
                i = self.compileTERM(tokens, i)
            xmlfile.write("</expression>\n")
        return i

    def compileTERM(self, tokens, i):
        with open(self.filename, 'a') as xmlfile:
            xmlfile.write("<term>\n")
            if i < len(tokens):
                if tokens[i].isdigit():
                    xmlfile.write(f"<integerConstant>{tokens[i]}</integerConstant>\n")
                    i += 1
                elif tokens[i][0] == '"' and tokens[i][-1] == '"':
                    xmlfile.write(f"<stringConstant>{tokens[i][1:-1]}</stringConstant>\n")
                    i += 1
                elif self.is_string_constant(tokens[i],i):
                    xmlfile.write(f"<keyword>{tokens[i]}</keyword>\n")
                    i += 1
                elif tokens[i] == "(":
                    xmlfile.write("<symbol>(</symbol>\n")
                    i += 1
                    i = self.compileEXPRESSION(tokens, i)
                    if i < len(tokens) and tokens[i] == ")":
                        xmlfile.write("<symbol>)</symbol>\n")
                        i += 1
                elif tokens[i] in analysetable.Operators:
                    xmlfile.write(f"<symbol>{tokens[i]}</symbol>\n")
                    i += 1
                    i = self.compileTERM(tokens, i)
                else:
                    # Assume it's an identifier
                    xmlfile.write(f"<identifier>{tokens[i]}</identifier>\n")
                    i += 1
                    if i < len(tokens) and tokens[i] == "[":
                        xmlfile.write("<symbol>[</symbol>\n")
                        i += 1
                        i = self.compileEXPRESSION(tokens, i)
                        if i < len(tokens) and tokens[i] == "]":
                            xmlfile.write("<symbol>]</symbol>\n")
                            i += 1
                    elif i < len(tokens) and tokens[i] in ["(", "."]:
                        i = self.compile_SUBROUTINE_CALL(tokens, i - 1)
            xmlfile.write("</term>\n")
        return i

    def compile_SUBROUTINE_CALL(self, tokens, i):
        with open(self.filename, 'a') as xmlfile:
            xmlfile.write(f"<identifier>{tokens[i]}</identifier>\n")
            i += 1
            if i < len(tokens) and tokens[i] == ".":
                xmlfile.write("<symbol>.</symbol>\n")
                i += 1
                xmlfile.write(f"<identifier>{tokens[i]}</identifier>\n")
                i += 1
            if i < len(tokens) and tokens[i] == "(":
                xmlfile.write("<symbol>(</symbol>\n")
                i += 1
                i = self.compile_EXPRESSION_LIST(tokens, i)
                if i < len(tokens) and tokens[i] == ")":
                    xmlfile.write("<symbol>)</symbol>\n")
                    i += 1
        return i

    def compile_EXPRESSION_LIST(self, tokens, i):
        with open(self.filename, 'a') as xmlfile:
            xmlfile.write("<expressionList>\n")
            if i < len(tokens) and tokens[i] != ")":
                i = self.compileEXPRESSION(tokens, i)
                while i < len(tokens) and tokens[i] == ",":
                    xmlfile.write("<symbol>,</symbol>\n")
                    i += 1
                    i = self.compileEXPRESSION(tokens, i)
            xmlfile.write("</expressionList>\n")
        return i

    def is_integer_constant(self, token, i):
        with open(self.filename, 'a') as xmlfile:
            if token.isdigit() and 0 <= int(token) <= 32767:
                xmlfile.write(f"<intconstant>{token}</intconstant>\n")
            else:
                return "not valid"
        return i

    def is_string_constant(self, token, i):
        with open(self.filename, 'a') as xmlfile:
            if token.startswith('"') and token.endswith('"') and '\n' not in token:
                xmlfile.write(f"<stringconstant>{token}</stringconstant>\n")
            else:
                return "not valid"
        return i

    def is_identifier(self, token, i):
        with open(self.filename, 'a') as xmlfile:
            if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', token) is not None:
                xmlfile.write(f"<identifier>{token}</identifier>\n")
            else:
                return "not valid"
        return i

    def advance(self, i):
        return i + 1