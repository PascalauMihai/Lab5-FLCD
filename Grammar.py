class Grammar:
    def __init__(self, givenFileName):
        self.fileName = givenFileName
        self.nonterminals = []
        self.terminals = []
        self.initialNonTerminal = ""
        self.productions = {}
        self.readInputFromFile()

    def readInitialNonTerminal(self, givenCurrentLine, givenFileReader):
        self.initialNonTerminal = givenCurrentLine[0:-1]
        currentLine = givenFileReader.readline()
        return currentLine, givenFileReader

    def readTerminals(self, givenCurrentLine, givenFileReader):
        self.terminals = givenCurrentLine.split(" ")
        self.terminals[-1] = self.terminals[-1][0:-1]
        currentLine = givenFileReader.readline()
        return currentLine, givenFileReader

    def readNonTerminals(self, givenCurrentLine, givenFileReader):
        self.nonterminals = givenCurrentLine.split(" ")
        self.nonterminals[-1] = self.nonterminals[-1][0:-1]
        currentLine = givenFileReader.readline()
        return currentLine, givenFileReader

    def readProductions(self, givenCurrentLine, givenFileReader):

        existingProductions = {}
        while givenCurrentLine:
            if givenCurrentLine == '\n':
                return givenCurrentLine, givenFileReader

            productionStart = givenCurrentLine.split("->")[0].strip()
            productionEnd = givenCurrentLine.split("->")[1].strip()

            if productionStart not in existingProductions:
                existingProductions[productionStart] = 1

            self.productions[(productionStart, existingProductions[productionStart])] = productionEnd
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
        print("Initial non terminal: " + self.initialNonTerminal)

    def printAllNonTerminals(self):
        print("Nonterminals: ", end="")
        for nonTerminal in self.nonterminals:
            print(nonTerminal + " ", end="")
        print()

    def printNonTerminal(self, givenTerminal):
        print("Nonterminal " + str(givenTerminal) + ":")

        for currentProduction in self.productions:
            if currentProduction[0] == givenTerminal:
                print(currentProduction[0] + str(currentProduction[1]) + " -> " +
                      self.productions[currentProduction])

        print()

    def printTerminals(self):
        print("Terminals: ", end="")
        for terminal in self.terminals:
            print(terminal + " ", end="")
        print()

    def printProductions(self):
        print("Productions:")
        for currentProduction in self.productions:
            print(currentProduction[0] + str(currentProduction[1]) + " -> " +
                  self.productions[currentProduction])
        print()

    def printAll(self):
        self.printInitialNonTerminal()
        self.printAllNonTerminals()
        self.printTerminals()
        self.printProductions()

    def printOneNonTerminal(self):
        inputNonTerminal = input("Enter one non terminal:")
        self.printNonTerminal(inputNonTerminal)


grammar = Grammar("g2.txt")

grammar.printAll()

grammar.printOneNonTerminal()
