import os
import memory_arithmetic.config as config
import re
import logging
import programmControl.regularexpressions as regularexpressions
import programmControl.fileprep as f

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s -- %(message)s -- (%(asctime)s)')

# Global variables
config.inputfile = None
config.outputfile = None

def is_folder(path):
    return os.path.isdir(path)

def process_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    validlines = []

    for line in lines:
        # Strip leading/trailing whitespace
        line = line.strip()
        
        # Check if the line contains any text after removing comments
        if not line.startswith("//") and line:
            # If the line has '//' but also contains alphanumeric characters, split it
            if "//" in line:
                parts = line.split("//")  # Split the line at '//'
                if re.search(r"[a-zA-Z]", parts[0]):  # Check if there are alphanumeric characters before the '//'
                    line = parts[0].strip()  # Keep only the part before '//'
            # Append the cleaned-up line
            validlines.append(line)

        # Remove inline comments
        if '//' in line:
            line = line.split('//')[0].strip()

        # Add non-empty lines to validlines
        if line:
            validlines.append(line)
    
	# saving folder of files
    filename = os.path.basename(file_path[:-3] + '.asm')
    dest = f"{config.outputfile}"
    if not os.path.exists(dest):
        os.mkdir(dest)
    output_path = os.path.join(dest, filename)

	# prepare variables & addreses in Asembly
    f.filepreparation(output_path)
    regularexpressions.functiondecider(validlines,output_path)
    return

def process_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.vm'):  
                vm_file_path = os.path.join(root, file)
                process_file(vm_file_path)
    return
