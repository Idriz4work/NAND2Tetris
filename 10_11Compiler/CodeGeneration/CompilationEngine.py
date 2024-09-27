import CodeGeneration.symboltable as SY, os, re, logging

classTable = SY.SymbolTABLES.SymbolTableCLASS
subroutineTable = SY.SymbolTABLES.SymbolTableSUBROUTINE

def startCompiling(values,output_path,filename):
	compiler = CompilationEngine(output_path, filename)
	logging.critical("COMPILATION ENGINE STARTS")
	compiler.compile(values)

class CompilationEngine:
	def __init__(self,filename,outputfolder):
		self.filename = filename
		self.output = outputfolder
		self.file = open(outputfolder,'a')

	def compile(self,values):
		i = 0
		while i < len(values):
			for value in values:
				num = ""
				if SY.SymbolTABLES.SymbolTableCLASS.getValues(value) == "not found":
					num = SY.SymbolTABLES.SymbolTableSUBROUTINE.getValues(value)
				if num == "not found":
					return "def compile : num not found"
			i = self.is_identifierVAS(number=num, i=i)

	def write(self,value):
		self.file.write(value)


	def compileSTATEMENTS(self, values, i):
		return i

	def compileSTATEMENT(self, values, i):
		return i + 1

	def compileIF(self, values, i):
		return i

	def compileWHILE(self, values, i):
		return i

	def compileLetSTATEMENT(self, values, i):    
		return i

	def compile_DO(self, values, i):
		return i

	def compile_RETURN(self, values, i):
		return i
	# The rest of the methods (compileEXPRESSION, compileTERM, etc.) remain the same
	# Just remember to remove any `if i < len(values):` checks at the beginning of these methods as well
	def compileEXPRESSION(self, values, i):
		return i

	def compileTERM(self, values, i):
		return i

	def compile_SUBROUTINE_CALL(self, values, i):
		return i

	def compile_EXPRESSION_LIST(self, values, i):
		return i

	def is_integer_constant(self, value, i):
		if int(value) <= 312435:
			self.write("")
		else:
			return "none valid"
		return i


	def is_string_constant(self, value, i):
		if value[0] != '_' or value[0] >= '0' and value[0] <= '9':
			if value >= 'a' and value <= 'z' or value >= 'A' and value <= 'Z':
				self.write("")
		else:
			return "none valid"
		return i

	# extend for var, argument, static, field, class & subroutine
	def is_identifierVAS(self, value,typee,number, i):
		# local, arg, static
		if value in ["var","argument","static"]:
			self.write(f"push {typee} {number}\n")
		i = CompilationEngine.advance(self=self,i=i)		
		return i

	def is_identifierFIELD():
		# field
		pass

	def is_identifierCLASS():
		# class

		# reset table to proceed new data
		classTable.reset()
		pass

	def is_identifierSUBROUTINE():
		# subroutine

		# reset table to proceed new data
		subroutineTable.reset()
		pass

	def compileARITHMETICS(self,value,i):
		if value == "+":
			self.write("add\n")
		if value == "-":
			self.write("sub\n")		
		if value == "*":
			self.write("Math.multiply\n")
		if value == "%":
			self.write("Math.remainder\n")
		if value == "/":
			self.write("Math.divide\n")
		else:
			return "none valid"
		
	def compileUnaryOPS(self,value,i):
		pass
	
	def advance(self, i):
		return i + 1