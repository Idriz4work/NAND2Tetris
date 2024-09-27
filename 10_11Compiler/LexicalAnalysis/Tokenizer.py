import os
import CodeGeneration.config as config
import logging
import LexicalAnalysis.JackGrammar as JackGrammar, LexicalAnalysis.CompilationEngine as CompilationEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s -- %(message)s -- (%(asctime)s)')

analysetable = JackGrammar.analyser_table

def Tokenizer(validlines, filepath):
    filename = os.path.splitext(os.path.basename(filepath))[0] + '.xml'
    dest = config.outputfile
    if not os.path.exists(dest):
        os.mkdir(dest)
    output_path = os.path.join(dest, filename)

    tokens = []
    logging.info("START TOKENIZING")
    for line in validlines:
        i = 0
        while i < len(line):
            char = line[i]
            # Skip whitespace
            if char.isspace():
                i += 1
                continue
            # Check for multi-character keywords and statements
            if line[i:].startswith("if"):
                tokens.append("if")
                i += 2
            elif line[i:].startswith("let"):
                tokens.append("let")
                i += 3
            elif line[i:].startswith("while"):
                tokens.append("while")
                i += 5
            elif line[i:].startswith("class"):
                tokens.append("class")
                i += 5
            elif line[i:].startswith("function"):
                tokens.append("function")
                i += 8
            elif line[i:].startswith("method"):
                tokens.append("method")
                i += 6
            # Check for single-character symbols
            elif char in "{}()[].,;+-*/&|<>=~":
                tokens.append(char)
                i += 1
            # Check for integer constants
            elif char.isdigit():
                num = ""
                while i < len(line) and line[i].isdigit():
                    num += line[i]
                    i += 1
                tokens.append(num)
            # Check for string constants
            elif char == '"':
                string = '"'
                i += 1
                while i < len(line) and line[i] != '"':
                    string += line[i]
                    i += 1
                if i < len(line):
                    string += '"'
                    i += 1
                tokens.append(string)
            # Check for identifiers (variable names)
            elif char.isalpha() or char == '_':
                identifier = ""
                while i < len(line) and (line[i].isalnum() or line[i] == '_'):
                    identifier += line[i]
                    i += 1
                tokens.append(identifier)
            else:
                # If no match is found, move to the next character
                logging.warning(f"Unrecognized character in line: [{char}] ({i})")
                i += 1

    CompilationEngine.startParsing(output_path=output_path, tokens=tokens, filename=filename)
    logging.info(f"Processed file: {filename}")
    return tokens
