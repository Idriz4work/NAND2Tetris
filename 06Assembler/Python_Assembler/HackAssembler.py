import os, re, logging
import argparse, shutil
import symboltable as cl

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s -- %(message)s -- (%(asctime)s)')

# Initialize symboltable instances
dest_table = cl.Dest()
comp_table = cl.CompTable()
jump_table = cl.Jump()

def parser(value,state):
	# c instructions
	if state == "c_instruction":
        # Initialize dest, comp, and jump
		dest, comp, jump = '', '', ''

        # Split the instruction
		parts = value.replace(' ', '').split('=')
		if len(parts) == 2:
			dest, rest = parts
		else:
			rest = parts[0]

		parts = rest.split(';')
		comp = parts[0]
		if len(parts) == 2:
			jump = parts[1]

        # Look up binary values
		dest_binary = dest_table.get_char(dest) if dest else dest_table.get_char('null')
		comp_binary = comp_table.get_char(comp)
		jump_binary = jump_table.get_char(jump) if jump else jump_table.get_char('null')

        # Check if all parts were found
		if 'Not found' in (dest_binary, comp_binary, jump_binary):
			return "Invalid instruction"
        # Construct the binary instruction
		a_bit = '1' if 'M' in comp else '0'
		result = f"111{a_bit}{comp_binary}{dest_binary}{jump_binary}"
		return result

	#symbol 	
	if state == "loop":
        # Construct the binary instruction
		bitrepresent = decimal_to_binary(value)
        # Check if all parts were found
		if 'Not found' in (bitrepresent):
			return "Invalid instruction"
		result = f"0{bitrepresent}"
		return result

	# symbol 
	if state == "variable":
        # Construct the binary instruction
		bitrepresent = decimal_to_binary(value)
        # Check if all parts were found
		if 'Not found' in (bitrepresent):
			return "Invalid instruction"
		result = f"0{bitrepresent}"
		return result
	
	# A instruction	
	if state ==  "a-instruction":
        # Construct the binary instruction
		bitrepresent = decimal_to_binary(value)
        # Check if all parts were found
		if 'Not found' in (bitrepresent):
			return "Invalid instruction"
		result = f"0{bitrepresent}"
		return result

# 15 bit 
def decimal_to_binary(n):
    try:
        # Convert input to integer if it's a string
        n = int(n)
        # Handle negative numbers
        if n < 0:
            # Use 2's complement for negative numbers
            n = (1 << 15) + n
        # Convert to binary and remove '0b' prefix
        binary = bin(n)[2:]
        
        # Pad with zeros to ensure 15-bit representation
        return binary.zfill(15)[-15:]
    except ValueError:
        # Return all zeros if input is not a valid number
        return "0" * 15
	
def main(filenameIN, filenameOUT):
	# 1. Input valid CHECK 
	# 2. Remove all the empty lines and comment lines from our code 
	# 3. With cleaned data, go through each string & check the symbol table with current code 
	# 4. Keep track of position CHECK 
	# 5. Convert the numbers to parser [010001010010] 
	# 6. put all together and write to HACKfile
	
	counter = 16
	position = 0

	# Open files
	asemblyfile = os.open(filenameIN, os.O_RDONLY)
	hackfile = os.open(filenameOUT, os.O_WRONLY | os.O_CREAT)	

	# REGULAR EXPRESSIONS
	# a_instructions syntax pattern
	a_instructionsyn = re.compile(r"^@\d+$")

	# Variable syntax pattern
	varisyn = re.compile(r"^@[a-zA-Z_.$:][a-zA-Z0-9_.$:]*$")

	# Loops syntax pattern
	loopsyn = re.compile(r"^\([^\)]*\)$")

	# skip empty lines and comments
	logging.info("Skipping whitespaces & comments...")
	with open(asemblyfile,'r') as file:
		valid_lines = [line.strip() for line in file if line.strip() and not line.strip().startswith('//')]

	# go through each line
	logging.info("validating data...")
	with open(hackfile,'w') as file:
		# second iteration
		for inside in valid_lines:
			result = 0
			
			# predefined @number/letter
			if a_instructionsyn.match(inside):
				logging.info("predef found")
				#
				result = parser(inside[1:],"a-instruction") # 1: becuae we skip @
				file.write(str(result)+ '\n')
				position += 1
				continue
			
			# variables
			if varisyn.match(inside):
				logging.info("variable found")
				#				
				result = parser(counter + position,"variable")
				file.write(str(result)+ '\n')
				counter += 1
				position += 1
				continue
			
			# loops
			if loopsyn.match(inside):
				logging.info("Loop found")
				#
				result = parser(position,"loop")
				file.write(str(result) + '\n')
				position += 1
				continue
			
			# goto statement D;JEQ ect..
			logging.info("c instruction found")
			result = parser(inside,"c_instruction")
			file.write(str(result)+ '\n')
			
			# file.write(inside)
			logging.info("counting...")
			position += 1
				
    # Create 'outputs' folder if it doesn't exist
	destination = "outputs"
	if not os.path.exists(destination):
	    os.mkdir(destination)

	# Move the output file to the 'outputs' folder
	shutil.move(filenameOUT, os.path.join(destination, filenameOUT))
	logging.critical("DONE ! Check code in outputs folder")

if __name__ == '__main__':
    putter = argparse.ArgumentParser()
    putter.add_argument('filenameIN', type=str, help='Enter the name of the assembly input file')
    putter.add_argument('filenameOUT', type=str, help='Enter the name of your hack output file')
    args = putter.parse_args()

    main(args.filenameIN, args.filenameOUT)
