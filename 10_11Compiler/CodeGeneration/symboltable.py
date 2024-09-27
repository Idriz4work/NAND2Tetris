import csv
import os
import logging

logging.basicConfig(level=logging.INFO, format='-- [%(levelname)s] -- %(message)s -- [%(filename)s : %(lineno)d] --')

class SymbolTABLES:

    @staticmethod
    def createNewTable(typee):
        if not os.path.exists("tableDATA"):
            os.mkdir("tableDATA")
        with open(f"tableDATA/data{typee.upper()}.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["NAME", "KIND", "TYPE", "NUMBER"])
        logging.info(f"Created new {typee} table")

    class SymbolTableSUBROUTINE:
        @staticmethod
        def getValues(name):
            with open("tableDATA/dataSUBROUTINE.csv", 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['NAME'] == name:
                        return row
            return "not found"

        @staticmethod
        def addValues(name, typee, kind):
            rows = []
            with open("tableDATA/dataSUBROUTINE.csv", 'r') as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                for row in rows:
                    if row['NAME'] == name:
                        return "value already in table"
                number = len(rows) + 1
            
            with open("tableDATA/dataSUBROUTINE.csv", 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([name, kind, typee, number])
            return "success"

        @staticmethod
        def reset():
            SymbolTABLES.createNewTable("subroutine")
            return "new table"

    class SymbolTableCLASS:
        @staticmethod
        def getValues(name):
            with open("tableDATA/dataCLASS.csv", 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['NAME'] == name:
                        return row
            return "not found"

        @staticmethod
        def addValues(name, typee, kind):
            rows = []
            with open("tableDATA/dataCLASS.csv", 'r') as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                for row in rows:
                    if row['NAME'] == name:
                        return "value already in table"
                number = len(rows) + 1
            
            with open("tableDATA/dataCLASS.csv", 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([name, kind, typee, number])
            return "success"

        @staticmethod
        def reset(name):
            SymbolTABLES.createNewTable(name)
            return "new table"