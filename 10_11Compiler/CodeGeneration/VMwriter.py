import os, re, logging, time, CodeGeneration.config as config
import CodeGeneration.symboltable as SY, CodeGeneration.CompilationEngine as cp
import LexicalAnalysis.JackGrammar as jg, CodeGeneration.symboltable as sy

analyse_table = jg.analyser_table

class_table = SY.SymbolTABLES.SymbolTableCLASS
subroutine_table = SY.SymbolTABLES.SymbolTableSUBROUTINE

logging.basicConfig(level=logging.INFO, format='-- %(levelname)s: %(message)s [%(filename)s:%(lineno)d] --')

# Example of logging
# logging.info("This is an informational message.")
# logging.error("This is an error message.")

def is_valid_identifier(value):
    pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
    return bool(re.match(pattern, value))

def is_integer_constant(value):
    try:
        int_value = int(value)
        return 0 <= int_value <= 32767
    except ValueError:
        return False

def is_string_constant(value):
    return value.startswith('"') and value.endswith('"')

def validator(lines, filepath):
    logging.info("START VALIDATING")
    
    valid_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        tokens = re.findall(r'\b\w+\b|\S', line)
        for token in tokens:
            if token in analyse_table.allSymbols:
                continue
            if (is_valid_identifier(token) or
                is_integer_constant(token) or
                is_string_constant(token) or
                token in ["var", "int", "string", "char", "Array", "let", "field", "static", "constructor", "class", "method"] or
                token in analyse_table.Operators):
                valid_lines.append(token)

    # Pass valid lines to VMwriter
    VMwriter(valid_lines=valid_lines, filepath=filepath)

def VMwriter(valid_lines, filepath):
    logging.critical("STARTING VM WRITER")
    
    try:
        filename = os.path.splitext(os.path.basename(filepath))[0] + '.vm'
        dest = config.outputfile
        
        if not os.path.exists(dest):
            os.mkdir(dest)
        if not os.path.exists("tableDATA"):
            sy.SymbolTABLES.createNewTable("class")
            sy.SymbolTABLES.createNewTable("subroutine")
        output_path = os.path.join(dest, filename)
        
        for token in valid_lines:
            if token in ["class", "method", "function", "constructor"]:
                current_scope = token
                continue

            if current_scope == "class":
                if token not in class_table.getValues(name=token):
                    class_table.addValues(name=token, kind="class", typee="class")
            elif current_scope in ["method", "function", "constructor"]:
                if token not in subroutine_table.getValues(name=token):
                    subroutine_table.addValues(name=token, kind="local", typee="var")

            # Here you can add more logic to handle different types of tokens
            # For example, handling variable declarations, function calls, etc.

        # Start compiling the valid lines
        cp.startCompiling(output_path=output_path,values=valid_lines,filename=filename)
    
    except Exception as e:
        print(f"FAIL VMWRITER: {e}\n")

