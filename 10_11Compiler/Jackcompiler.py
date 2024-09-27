import CodeGeneration.config as config
import logging
import argparse
import LexicalAnalysis.handelingInput as handelingInput

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s -- %(message)s -- (%(asctime)s)')
# Global variables
config.inputfile = None
config.outputfile = None

def main():
    if config.inputfile is None:
        logging.error("Input file or folder not specified")
        return
    if handelingInput.is_folder(config.inputfile):
        handelingInput.process_folder(config.inputfile)
    else:
        handelingInput.process_file(config.inputfile)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", type=str, help="USAGE: [INPUT] [OUTPUT]")
    parser.add_argument("outputfile", type=str, help="USAGE: [INPUT] [OUTPUT]")
    args = parser.parse_args()

    config.inputfile = args.inputfile
    config.outputfile = args.outputfile

    main()
