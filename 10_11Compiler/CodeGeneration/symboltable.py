import os
import csv
import logging

class SymbolTables:

    @staticmethod
    def create_new_table(table_type):
        if not os.path.exists("tableDATA"):
            os.mkdir("tableDATA")
        with open(f"tableDATA/data{table_type}.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["NAME", "TYPE", "KIND", "NUMBER"])
            writer.writerow(["this","Point","argument","0"])
        logging.info(f"Created new {table_type} table")

    class SymbolTableSubroutine:
        @staticmethod
        def getValues(name):
            with open("tableDATA/dataSUBROUTINE.csv", 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['NAME'] == name:
                        return row
            return None

        @staticmethod
        def addValues(name, kind, typee):
            with open("tableDATA/dataSUBROUTINE.csv", 'r') as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                for row in rows:
                    if row['NAME'] == name:
                        return "Value already in table"
                number = len(rows) + 1
            
            with open("tableDATA/dataSUBROUTINE.csv", 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([name, kind, typee, str(number)])
            return "Success"

        @staticmethod
        def reset():
            SymbolTables.create_new_table("subroutine")
            return "New subroutine table created"

    class SymbolTableClass:
        @staticmethod
        def getValues(name):
            with open("tableDATA/dataCLASS.csv", 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['NAME'] == name:
                        return row
            return None

        @staticmethod
        def addValues(name, kind, typee):
            with open("tableDATA/dataCLASS.csv", 'r') as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                for row in rows:
                    if row['NAME'] == name:
                        return "Value already in table"
                number = len(rows) + 1
            
            with open("tableDATA/dataCLASS.csv", 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([name, kind, typee, str(number)])
            return "Success"

        @staticmethod
        def reset():
            SymbolTables.create_new_table("class")
            return "New class table created"

    @staticmethod
    def is_statementS(values, i):
        if i >= len(values):
            return "valid", i
        
        result, new_i = SymbolTables.is_statement(values, i)
        if result == "valid":
            result, new_i = SymbolTables.is_statementS(values, new_i)
        
        return result, new_i

    @staticmethod
    def is_statement(values, i):
        if i >= len(values):
            return "not valid", i
        
        if values[i] == "if":
            return SymbolTables.is_ifstatement(values, i + 1)
        elif values[i] == "while":
            return SymbolTables.is_whilestatement(values, i + 1)
        elif values[i] == "let":
            return SymbolTables.is_letstatement(values, i + 1)
        else:
            return "not valid", i

    @staticmethod
    def is_whilestatement(values, i):
        if i >= len(values) or values[i] != '(':
            return "not valid", i
        
        result, new_i = SymbolTables.is_expression(values, i + 1)
        if result == "not valid":
            return "not valid", new_i
        
        if new_i >= len(values) or values[new_i] != ')':
            return "not valid", new_i
        
        if new_i + 1 >= len(values) or values[new_i + 1] != '{':
            return "not valid", new_i + 1
        
        result, new_i = SymbolTables.is_statementS(values, new_i + 2)
        if result == "not valid":
            return "not valid", new_i
        
        if new_i >= len(values) or values[new_i] != '}':
            return "not valid", new_i
        
        return "valid", new_i + 1

    @staticmethod
    def is_ifstatement(values, i):
        if i >= len(values) or values[i] != '(':
            return "not valid", i
        
        result, new_i = SymbolTables.is_expression(values, i + 1)
        if result == "not valid":
            return "not valid", new_i
        
        if new_i >= len(values) or values[new_i] != ')':
            return "not valid", new_i
        
        if new_i + 1 >= len(values) or values[new_i + 1] != '{':
            return "not valid", new_i + 1
        
        result, new_i = SymbolTables.is_statementS(values, new_i + 2)
        if result == "not valid":
            return "not valid", new_i
        
        if new_i >= len(values) or values[new_i] != '}':
            return "not valid", new_i
        
        return "valid", new_i + 1

    @staticmethod
    def is_letstatement(values, i):
        name, new_i = SymbolTables.is_Name(values, i)
        if name == "not a valid name":
            return "error name", new_i
        
        if new_i >= len(values):
            return "op error", new_i
        
        op = SymbolTables.is_op(values[new_i])
        if op == "not valid":
            return "op error", new_i
        
        result, new_i = SymbolTables.is_expression(values, new_i + 1)
        if result == "not valid":
            return "error expression", new_i
        
        if new_i >= len(values) or values[new_i] != ';':
            return "missing semicolon", new_i
        
        return "valid", new_i + 1

    @staticmethod
    def is_Name(values, i):
        if i >= len(values):
            return "not a valid name", i
        if SymbolTables.is_valid_name(values[i]):
            return values[i], i + 1
        return "not a valid name", i

    @staticmethod
    def is_expression(values, i):
        result, new_i = SymbolTables.is_term(values, i)
        if result == "not valid":
            return "not valid", new_i

        # Handle binary operator expressions
        while new_i < len(values) and SymbolTables.is_op(values[new_i]) != "not valid":
            result, new_i = SymbolTables.is_term(values, new_i + 1)
            if result == "not valid":
                return "not valid", new_i
        
        return "valid", new_i

    @staticmethod
    def is_term(values, i):
        if i >= len(values):
            return "not valid", i
        
        if SymbolTables.is_valid_name(values[i]) or SymbolTables.is_constant(values[i]) or values[i] in ['true', 'false', 'null', 'this']:
            return "valid", i + 1
        
        return "not valid", i

    @staticmethod
    def is_valid_name(name):
        return name.isidentifier()

    @staticmethod
    def is_constant(value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_op(op):
        return op in ['+', '-', '=', '<', '>', '*', '/']
