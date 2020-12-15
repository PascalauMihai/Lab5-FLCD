class ParserOutput:
    def __init__(self, givenOutputFileName, grammar):
        self.__output = []
        self.fileName = givenOutputFileName
        self.productionString = ""
        self.derivations = ""
        self.derivationString = ""
        self.grammar = grammar

    def setParserResult(self, givenResult):
        self.__output = givenResult

    def setDerivationsResult(self, givenDerivationStringResult):
        self.derivations = givenDerivationStringResult

    def setResultAndCalculateProductionString(self, givenResult, givenDerivations):
        self.setParserResult(givenResult)
        self.setDerivationsResult(givenDerivations)
        self.calculateProductionString()
        self.calculateDerivationString()

    def calculateDerivationString(self):
        result = []
        currentList = [self.__output.pop(0)]
        headList = []
        while self.__output:
            index = 0
            elementsAdded = 0
            currentLength = len(self.grammar.getProductions()[currentList[0]])
            while elementsAdded < currentLength and index < len(self.__output):
                if self.__output[index] in self.grammar.getTerminals():
                    currentList.append(self.__output.pop(index))
                    elementsAdded += 1
                else:
                    toAdd = len(self.grammar.getProductions()[self.__output[index]])
                    currentList.append(self.__output.pop(index))
                    elementsAdded += 1
                    parseToAdd = toAdd + index
                    while index < parseToAdd and index < len(self.__output):
                        if self.__output[index][0] in self.grammar.getNonTerminals():
                            parseToAdd += len(self.grammar.getProductions()[self.__output[index]])
                        index += 1
            result.append(currentList)
            index = 1
            added = 0
            while index < len(result[-1]):
                if result[-1][index] in self.grammar.getProductions():
                    if added == 0:
                        currentList = [result[-1][index]]
                        added = 1
                    elif added == 1:
                        headList.append(result[-1][index])
                index += 1
            if added == 0 and self.__output:
                currentList = [headList.pop(0)]

        steps = len(result) - 1
        currentStep = 0
        start = result[0].pop(0)
        self.derivationString += start[0] + str(start[1]) + " "
        currentList = result[0]
        addedTuples = 1
        while currentStep < steps:
            self.derivationString += "=> "
            newList = []
            index = 0
            while index < len(currentList):
                if isinstance(currentList[index], tuple):
                    self.derivationString += currentList[index][0] + str(currentList[index][1]) + " "
                    newList += result[addedTuples][1:]
                    addedTuples += 1
                else:
                    if currentList[index] != 'epsilon':
                        self.derivationString += currentList[index] + " "
                        newList.append(currentList[index])
                index += 1
            currentList = newList
            currentStep += 1

    def calculateProductionString(self):
        for element in self.__output:
            if isinstance(element, tuple):
                self.productionString += element[0] + str(element[1]) + " "

    def printProductionString(self):
        print("Production string: " + self.productionString)

    def printDerivationString(self):
        print("Derivation string: " + self.derivationString)

    def writeRepresentationsToFile(self, code):
        with open(self.fileName, 'w') as filePath:
            if code == "error":
                filePath.write("Error, not finished representations!!!!!!\n")
            filePath.write(
                "Production string: " + self.productionString + "\n")
            filePath.write("Derivation string: " + self.derivationString + "\n")
            filePath.write("Derivations: " + self.derivations)

