import os
import re
import logging
import time
import CodeGeneration.config as config
import CodeGeneration.symboltable as SY
import CodeGeneration.CompilationEngine as cp
import LexicalAnalysis.JackGrammar as jg

# Analyser table imported from JackGrammar
analyse_table = jg.analyser_table

# Class and subroutine symbol tables
class_table = SY.SymbolTables.SymbolTableClass
subroutine_table = SY.SymbolTables.SymbolTableSubroutine

# Logging configuration
logging.basicConfig(level=logging.INFO, format='-- %(levelname)s: %(message)s [%(filename)s:%(lineno)d] --')

# Validation functions
def is_valid_identifier(value):
    pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
    return bool(re.match(pattern, value))

def is_integer_constant(value):
    try:
        int_value = int(value)
        if 0 <= int_value <= 32767:
            return str(int_value)
        else:
            return 'false'
    except ValueError:
        return 'false'

def is_string_constant(value):
    return value.startswith('"') and value.endswith('"')

def checkTYPE(lines, index):
    Type = ''
    if lines[index] in ["var", "int", "string", "char", "Array", "let", "field", "static"]:
        Type = lines[index]
        return Type
    else:
        return "no valid Type"

# VMWriter function
def VMwriter(valid_lines, filepath):
    logging.critical("STARTING VM WRITER")
    i = 0    
    current_scope = None  # Initialize current_scope

    # Prepare the filename for output
    filename = os.path.splitext(os.path.basename(filepath))[0] + '.vm'
    dest = config.outputfile

    # Create output directory if it doesn't exist
    if not os.path.exists(dest):
        os.mkdir(dest)

    # Create the symbol table directory if it doesn't exist
    if not os.path.exists("tableDATA"):
        SY.SymbolTables.create_new_table("subroutine")
        SY.SymbolTables.create_new_table("class")
    
    output_path = os.path.join(dest, filename)
    try:
        while i < len(valid_lines):
            token = valid_lines[i]
            
            # Detect scope (class, method, function, constructor)
            if token in ["class", "method", "function", "constructor"]:
                current_scope = token  # Update the current scope
                i += 1
                continue

            # Handle class scope
            if current_scope == "class":
                class_name = valid_lines[i]
                if not class_table.getValues(class_name):
                    logging.info("class table add value")
                    class_table.addValues(name=class_name, kind="class", typee="class")
                    cp.CompilationEngine.compile(self=cp.CompilationEngine(output_path=output_path,filename=filename,values=valid_lines),typename=class_name,values=valid_lines)
                i += 1  # Skip the class name token after processing

            # Handle method, function, or constructor scope
            elif current_scope in ["method", "function", "constructor"]:
                subroutine_name = valid_lines[i]
                if not subroutine_table.getValues(subroutine_name):
                    logging.info("subroutine table add value")
                    subroutine_table.addValues(name=subroutine_name, kind="local", typee="var")
                    cp.CompilationEngine.compile(self=cp.CompilationEngine(output_path=output_path,filename=filename,values=valid_lines),typename=subroutine_name,values=valid_lines)
                i += 1  # Skip the subroutine name token after processing

            i += 1  # Increment index after each token is processed

    except FileNotFoundError as fnf_error:
        logging.error(f"File not found: {fnf_error}")
    except IOError as io_error:
        logging.error(f"Input/output error: {io_error}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

