import os
import config
import logging
import JackGrammar, Tokenizer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s -- %(message)s -- (%(asctime)s)')

analysetable = JackGrammar.analyser_table

import os
import logging
import config
import Tokenizer

# Global variables
config.inputfile = None
config.outputfile = None

def is_folder(path):
    return os.path.isdir(path)

def process_file(file_path):
    logging.info(f"Processing file: {file_path}")
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

        validlines = []
        in_multiline_comment = False

        for line in lines:
            line = line.strip()
            # Handle multi-line comments
            if line.startswith('/**') or line.startswith('/*'):
                in_multiline_comment = True
                continue
            if line.endswith('*/'):
                in_multiline_comment = False
                continue
            if in_multiline_comment:
                continue

            # Remove inline comments
            if '//' in line:
                line = line.split('//')[0].strip()

            # Add non-empty lines to validlines
            if line:
                validlines.append(line)

        Tokenizer.Tokenizer(validlines, file_path)
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {str(e)}")

def process_folder(folder_path):
    logging.info(f"Processing folder: {folder_path}")
    if not os.path.exists(folder_path):
        logging.error(f"Folder does not exist: {folder_path}")
        return

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.jack'):
                file_path = os.path.join(root, file)
                logging.debug(f"Found .jack file: {file_path}")
                process_file(file_path)