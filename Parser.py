from Grammar import Grammar
from ParserOutput import ParserOutput


class Parser:
    def __init__(self, grammarFileName, givenParserOutputName):
        self.currentState = 'q'
        self.index = 0
        self.workingStack = []
        self.grammar = Grammar(grammarFileName)
        self.parserOutput = ParserOutput(givenParserOutputName)
        self.debug = True
        self.inputStack = []
        self.epsilonCount = 0
        self.derivationsString = ""

    def printAll(self):
        print("-----------------------------------------------------------------------------------")
        print("Current state: " + self.currentState)
        print("Current index: " + str(self.index))
        print("Working stack: " + str(self.workingStack))
        print("Input stack: " + str(self.inputStack))

    def expand(self):
        if isinstance(self.inputStack[0], tuple):
            nonterminal = self.inputStack.pop(0)
        elif isinstance(self.inputStack[0], list):
            nonterminal = (self.inputStack[0].pop(0), 1)
            if len(self.inputStack[0]) == 0:
                self.inputStack.pop(0)
        else:
            nonterminal = (self.inputStack.pop(0), 1)

        self.workingStack.append(nonterminal)
        newProduct = self.grammar.getProductions()[nonterminal]
        self.inputStack.insert(0, newProduct)

    def advance(self):
        self.index += 1
        if isinstance(self.inputStack[0], tuple):
            terminal = self.inputStack[0].pop(0)
        elif isinstance(self.inputStack[0], list):
            terminal = self.inputStack[0].pop(0)
            if len(self.inputStack[0]) == 0:
                self.inputStack.pop(0)
        else:
            terminal = self.inputStack.pop(0)

        self.workingStack.append(terminal)

    def momentaryInsucces(self):
        self.currentState = 'b'

    def back(self):
        self.index -= 1
        lastFromWorkingStack = [self.workingStack.pop()]
        if lastFromWorkingStack == ['epsilon']:
            self.epsilonCount -= 1
        self.inputStack.insert(0, lastFromWorkingStack)

    def anotherTry(self):
        lastFromWorkingStack = self.workingStack.pop()
        checkIfNextExists = (lastFromWorkingStack[0], lastFromWorkingStack[1] + 1)
        if checkIfNextExists in self.grammar.getProductions():
            self.currentState = 'q'
            self.workingStack.append(checkIfNextExists)

            removedElements = 0
            while removedElements < len(self.grammar.getProductions()[lastFromWorkingStack]):
                if isinstance(self.inputStack[0], list):
                    if len(self.inputStack[0]) == 1:
                        self.inputStack.pop(0)
                        removedElements += 1
                    else:
                        while len(self.inputStack[0]) > 0 and removedElements < \
                                len(self.grammar.getProductions()[lastFromWorkingStack]):
                            self.inputStack[0].pop(0)
                            removedElements += 1
                        if len(self.inputStack[0]) == 0:
                            self.inputStack.pop(0)
                else:
                    self.inputStack.pop(0)
                    removedElements += 1

            self.inputStack.insert(0, self.grammar.getProductions()[checkIfNextExists])
        elif self.index == 0 and lastFromWorkingStack[0] == self.grammar.getInitialNonTerminal():
            self.currentState = 'e'
        else:
            removedElements = 0
            while removedElements < len(self.grammar.getProductions()[lastFromWorkingStack]):
                if isinstance(self.inputStack[0], list):
                    if len(self.inputStack[0]) == 1:
                        self.inputStack.pop(0)
                        removedElements += 1
                    else:
                        while len(self.inputStack[0]) > 0 and removedElements < \
                                len(self.grammar.getProductions()[lastFromWorkingStack]):
                            self.inputStack[0].pop(0)
                            removedElements += 1
                        if len(self.inputStack[0]) == 0:
                            self.inputStack.pop(0)
                else:
                    self.inputStack.pop(0)
                    removedElements += 1
            self.inputStack.insert(0, [lastFromWorkingStack[0]])

    def success(self):
        self.currentState = 'f'
        self.index += 1

    def checkWordLength(self, w):
        if len(w) > self.index - self.epsilonCount:
            if self.inputStack[0][0] == 'epsilon':
                self.epsilonCount += 1
                return True
            if self.inputStack[0][0] in self.grammar.getNonTerminals():
                return True
            return self.inputStack[0][0] == w[self.index - self.epsilonCount]
        return False

    def addOneStepDerivationString(self):
        oneStepDerivationString = "(" + self.currentState + ", " + str(self.index) + ", " + str(self.workingStack) + \
                                  ", " + str(self.inputStack) + ")\n"

        self.derivationsString += oneStepDerivationString

    def runAlgorithm(self, w):
        self.currentState = 'q'
        self.index = 0
        self.workingStack = []
        self.debug = True
        self.inputStack = [(self.grammar.getInitialNonTerminal(), 1)]
        self.epsilonCount = 0
        self.derivationsString = ""

        while self.currentState != "f" and self.currentState != "e":
            if self.debug:
                self.printAll()

            self.addOneStepDerivationString()
            if self.currentState == "q":
                if len(self.inputStack) == 0 and self.index - self.epsilonCount == len(w):
                    self.derivationsString += "|- succ"
                    self.currentState = "f"
                else:
                    if len(self.inputStack) > 0 and self.inputStack[0][0] in self.grammar.getNonTerminals():
                        self.derivationsString += "|- exp"
                        self.expand()
                    elif len(self.inputStack) > 0 and self.inputStack[0][0] in self.grammar.getTerminals() \
                            and self.checkWordLength(w):
                        self.derivationsString += "|- adv"
                        self.advance()
                    else:
                        self.derivationsString += "|- mi"
                        self.momentaryInsucces()
            elif self.currentState == "b":
                if self.workingStack[-1] in self.grammar.getTerminals():
                    self.derivationsString += "|- bk"
                    self.back()
                else:
                    self.derivationsString += "|- at"
                    self.anotherTry()

        self.addOneStepDerivationString()
        if self.currentState == "e":
            print("Error")
            self.parserOutput.setDerivationStringResult(self.derivationsString)
            self.parserOutput.printDerivationString()
        else:
            print("Finished")
            self.parserOutput.setParserResult(self.workingStack)
            self.parserOutput.setDerivationStringResult(self.derivationsString)
            self.parserOutput.calculateProductionString()
            self.parserOutput.printProductionString()
            self.parserOutput.printDerivationString()
            self.parserOutput.writeRepresentationsToFile()


def generateInputFromPIF(givenFileName):
    output = []
    with open(givenFileName, 'r') as filePath:
        currentLine = filePath.readline()
        while currentLine:
            element = currentLine.split(" ")[0]
            index = 0
            while index < len(element) and element[index] != '\'':
                index += 1

            element = element[index + 1:]
            index = len(element) - 1
            while index >= 0 and element[index] != '\'':
                index -= 1
            element = element[:index]
            output.append(element)
            currentLine = filePath.readline()

    print(output)
    return output


parser = Parser("g2.txt", "out2.txt")

# generateInputFromPIF("lab3/PIF.out")

parser.runAlgorithm(['a', 'a', 'c', 'b', 'c'])
# parser.runAlgorithm(["integer", "mainFunction", "(",  "integer", "identifier", ")", "{", "readFromKeyboard", ">>", "identifier", ";", "return", "constant", ";", "}"])
# parser.runAlgorithm(["integer", "mainFunction", "(", ")", "{","readFromKeyboard", ">>","identifier", ">>", "identifier",
# ">>", "identifier", ";", "}"])
parser.runAlgorithm(generateInputFromPIF("lab3/PIF.out"))
