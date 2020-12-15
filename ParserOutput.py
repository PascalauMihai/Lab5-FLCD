class ParserOutput:
    def __init__(self, givenOutputFileName):
        self.__output = []
        self.fileName = givenOutputFileName
        self.productionString = ""
        self.derivationString = ""

    def setParserResult(self, givenResult):
        self.__output = givenResult

    def setDerivationStringResult(self, givenDerivationStringResult):
        self.derivationString = givenDerivationStringResult

    def calculateProductionString(self):
        for element in self.__output:
            if isinstance(element, tuple):
                self.productionString += element[0] + str(element[1]) + " "

    def printProductionString(self):
        print("Production string: " + self.productionString)


    def printDerivationString(self):
        print("Derivation string: " + self.derivationString)


    def writeRepresentationsToFile(self):
        with open(self.fileName, 'w') as filePath:
            filePath.write(
                "Production string: " + self.productionString + "\n")
            filePath.write("Derivation string: " + self.derivationString + "\n")