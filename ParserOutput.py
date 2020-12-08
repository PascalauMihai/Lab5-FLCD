class ParserOutput:
    def __init__(self):
        self.__output = []
        self.productionString = ""

    def setParserResult(self, givenResult):
        self.__output = givenResult

    def calculateProductionString(self):
        for element in self.__output:
            if isinstance(element, tuple):
                self.productionString += element[0] + str(element[1]) + " "

    def printProductionString(self):
        print("Production string: " + self.productionString)

