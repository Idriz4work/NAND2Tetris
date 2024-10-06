import memory_arithmetic.config as config
import logging
import argparse
import programmControl.handelingInput as handelingInput

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s -- %(message)s -- (%(asctime)s)')

# -------------------------- #

def main():
    # Go through each line, remove whitespaces, and filter comments
    if handelingInput.is_folder(config.inputfile):
        handelingInput.process_folder(config.inputfile)
    else:
        handelingInput.process_file(config.inputfile)
                    
    logging.critical("SUCCESS: translated VMcode into ASM\n")
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", type=str, help="USAGE: [INPUT] [OUTPUT]")
    parser.add_argument("outputfile", type=str, help="USAGE: [INPUT] [OUTPUT]")
    args = parser.parse_args()
    
    config.inputfile = args.inputfile
    config.outputfile = args.outputfile
    
    main()
