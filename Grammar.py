import copy

class Grammar:
    def __init__(self, givenFileName):
        self.fileName = givenFileName
        self.__nonterminals = []
        self.__terminals = []
        self.__initialNonTerminal = ""
        self.__productions = {}
        self.readInputFromFile()

    def getNonTerminals(self):
        return self.__nonterminals

    def getProductions(self):
        return copy.deepcopy(self.__productions)

    def getTerminals(self):
        return self.__terminals

    def getInitialNonTerminal(self):
        return self.__initialNonTerminal

    def readInitialNonTerminal(self, givenCurrentLine, givenFileReader):
        self.__initialNonTerminal = givenCurrentLine[0:-1]
        currentLine = givenFileReader.readline()
        return currentLine, givenFileReader

    def readTerminals(self, givenCurrentLine, givenFileReader):
        self.__terminals = givenCurrentLine.split(" ")
        self.__terminals[-1] = self.__terminals[-1][0:-1]
        currentLine = givenFileReader.readline()
        return currentLine, givenFileReader

    def readNonTerminals(self, givenCurrentLine, givenFileReader):
        self.__nonterminals = givenCurrentLine.split(" ")
        self.__nonterminals[-1] = self.__nonterminals[-1][0:-1]
        currentLine = givenFileReader.readline()
        return currentLine, givenFileReader

    def readProductions(self, givenCurrentLine, givenFileReader):

        existingProductions = {}
        while givenCurrentLine:
            if givenCurrentLine == '\n':
                return givenCurrentLine, givenFileReader

            productionStart = givenCurrentLine.split("->")[0].strip()
            productionEnd = list(givenCurrentLine.split("->")[1].strip().split(" "))

            if productionStart not in existingProductions:
                existingProductions[productionStart] = 1

            self.__productions[(productionStart, existingProductions[productionStart])] = productionEnd
            existingProductions[productionStart] += 1

            givenCurrentLine = givenFileReader.readline()

        return givenCurrentLine, givenFileReader

    def readInputFromFile(self):
        with open(self.fileName, 'r') as fileReader:
            currentLine = fileReader.readline()
            lineNumber = 1
            switchCase = {
                1: self.readInitialNonTerminal,
                2: self.readNonTerminals,
                3: self.readTerminals,
                4: self.readProductions
            }
            while currentLine:
                if lineNumber not in switchCase:
                    print("Error: invalid input. Line - ", lineNumber)
                currentReadFunction = switchCase[lineNumber]
                currentLine, fileReader = currentReadFunction(currentLine, fileReader)
                lineNumber += 1

    def printInitialNonTerminal(self):
        print("Initial non terminal: " + self.__initialNonTerminal)

    def printAllNonTerminals(self):
        print("Nonterminals: ", end="")
        for nonTerminal in self.__nonterminals:
            print(nonTerminal + " ", end="")
        print()

    def printNonTerminal(self, givenTerminal):
        print("Nonterminal " + str(givenTerminal) + ":")

        for currentProduction in self.__productions:
            if currentProduction[0] == givenTerminal:
                print(currentProduction[0] + str(currentProduction[1]) + " -> " +
                      self.__productions[currentProduction])

        print()

    def printTerminals(self):
        print("Terminals: ", end="")
        for terminal in self.__terminals:
            print(terminal + " ", end="")
        print()

    def printProductions(self):
        print("Productions:")
        for currentProduction in self.__productions:
            print(currentProduction[0] + str(currentProduction[1]) + " -> " +
                  str(self.__productions[currentProduction]))
        print()

    def printAll(self):
        self.printInitialNonTerminal()
        self.printAllNonTerminals()
        self.printTerminals()
        self.printProductions()

    def printOneNonTerminal(self):
        inputNonTerminal = input("Enter one non terminal:")
        self.printNonTerminal(inputNonTerminal)



#grammar = Grammar("g1.txt")

#grammar.printAll()
#print(grammar.productions)
#grammar.printOneNonTerminal()
