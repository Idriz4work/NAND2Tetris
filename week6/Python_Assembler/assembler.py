import os, re, logging, datetime
import argparse, shutil
import symboltable as cl

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s -- %(message)s -- (%(asctime)s)')

# Initialize table instances
dest_table = cl.Dest()
comp_table = cl.CompTable()
jump_table = cl.Jump()
symbol_table = cl.SymbolTable()

vari = cl.variabless("","",0,[])
predef = cl.Symbol("","",0,False,False)
loop = cl.loops("","",0,"")

def binary(value,state):
	if state == "goto":
		for key,value in comp_table.codes.items():
			if value == key:
				comp = value
			comp = "000000"
		for key,value in jump_table.codes.items():
			if value == key:
				jump = value 
			jump = "000"
		result = f"111{comp}{jump}"
		return (result)
	if state == "loop":
		

def parser(inside):
	pass
	
def main(filenameIN, filenameOUT):
	# 1. Input valid CHECK 
	# 2. Remove all the empty lines and comment lines from our code 
	# 3. With cleaned data, go through each string & check the symbol table with current code 
	# 4. Keep track of position CHECK 
	# 5. Convert the numbers to binary [010001010010] 
	# 6. put all together and write to HACKfile
	
	counter = 16
	position = 0

	# Open files
	asemblyfile = os.open(filenameIN, os.O_RDONLY)
	hackfile = os.open(filenameOUT, os.O_WRONLY | os.O_CREAT)	

	# REGULAR EXPRESSIONS
	# Predefined syntax pattern
	predef = re.compile(r"^@\d+$")

	# Variable syntax pattern
	varisyn = re.compile(r"^@[a-zA-Z_.$:][a-zA-Z0-9_.$:]*$")

	# Loops syntax pattern
	loopsyn = re.compile(r"^\([^\)]*\)$")

	# Goto statement pattern
	goto = re.compile(r"^[A-Za-z0-9_.$:]+;[A-Z]{3}$")

	# skip empty lines and comments
	logging.info("Skipping whitespaces & comments...")
	with open(asemblyfile,'r') as file:
		valid_lines = [line.strip() for line in file if line.strip() and not line.strip().startswith('//')]

	# go through each line
	logging.info("validating data...")
	with open(hackfile,'w') as file:
		for inside in valid_lines:
			# loops
			if loopsyn.match(inside):
				logging.info("Loop found")
				loop.name = inside[1:-1]
				loop.address = position
				symbol_table.add_symbol(name=loop.name,address=loop.address)
			
				result = binary(inside,"loop")
				file.write(str(result) + '\n')
				position += 1
				continue
			
			# @ declarations
			if varisyn.match(inside):
				logging.info("variable found")
				vari.name = inside[0:-1]
				vari.address = counter
				symbol_table.add_symbol(name=vari.name,address=vari.address)
				
				result = binary(inside,"variable")
				file.write(str(result)+ '\n')
				counter += 1
				position += 1
				continue

			# predefined 
			if predef.match(inside):
				logging.info("predef found")
				predef.name = inside[0:-1]
				predef.address = position
				symbol_table.add_symbol(name=predef.name,address=predef.address)
				
				result = binary(inside,"predef")
				file.write(str(result)+ '\n')
				position += 1
				continue
			# goto statement D;JEQ ect..
			if goto.match(inside):
				logging.info("goto found")
				parser(inside)
				result = binary(inside,"goto")
				file.write(str(result)+ '\n')

			# file.write(inside)
			logging.fatal("nothing found")
			position += 1

    # Create 'outputs' folder if it doesn't exist
	destination = "outputs"
	if not os.path.exists(destination):
	    os.mkdir(destination)

	logging.info("DONE ! Check code in outputs folder")
	# Move the output file to the 'outputs' folder
	shutil.move(filenameOUT, os.path.join(destination, filenameOUT))



if __name__ == '__main__':
    putter = argparse.ArgumentParser()
    putter.add_argument('filenameIN', type=str, help='Enter the name of the assembly input file')
    putter.add_argument('filenameOUT', type=str, help='Enter the name of your hack output file')
    args = putter.parse_args()

    main(args.filenameIN, args.filenameOUT)


