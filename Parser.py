from Grammar import Grammar
from ParserOutput import ParserOutput

class Parser:
    def __init__(self, grammarFileName):
        self.currentState = 'q'
        self.index = 0
        self.workingStack = []
        self.grammar = Grammar(grammarFileName)
        self.parserOutput = ParserOutput()
        self.debug = True
        self.inputStack = []

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

      #  if terminal == 'epsilon':
      #      self.workingStack.pop()
      #  else:
        self.workingStack.append(terminal)

    def momentaryInsucces(self):
        self.currentState = 'b'

    def back(self):
        self.index -= 1
        lastFromWorkingStack = [self.workingStack.pop()]
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
            self.inputStack.pop(0)
            self.inputStack.insert(0, lastFromWorkingStack[0])

    def success(self):
        self.currentState = 'f'
        self.index += 1

    def checkWordLength(self, w):
        if len(w) > self.index:
            if self.inputStack[0][0] == 'epsilon':
                return True
            return self.inputStack[0][0] == w[self.index]
        return False

    def runAlgorithm(self, w):
        self.currentState = 'q'
        self.index = 0
        self.workingStack = []
        self.debug = True
        self.inputStack = [(self.grammar.getInitialNonTerminal(), 1)]

        while self.currentState != "f" and self.currentState != "e":
            if self.debug:
                self.printAll()

            if self.currentState == "q":
                if len(self.inputStack) == 0 and self.index == len(w):
                    self.currentState = "f"
                else:
                    if len(self.inputStack) > 0 and self.inputStack[0][0] in self.grammar.getNonTerminals():
                        self.expand()
                    elif len(self.inputStack) > 0 and self.inputStack[0][0] in self.grammar.getTerminals() \
                            and self.checkWordLength(w):
                        self.advance()
                    else:
                        self.momentaryInsucces()
            elif self.currentState == "b":
                if self.workingStack[-1] in self.grammar.getTerminals():
                    self.back()
                else:
                    self.anotherTry()
        if self.currentState == "e":
            print("Error")
        else:
            print("Finished")
            print(self.workingStack)
            self.parserOutput.setParserResult(self.workingStack)
            self.parserOutput.calculateProductionString()
            self.parserOutput.printProductionString()


def generateInputFromPIF(givenFileName):
    output = []
    with open(givenFileName, 'r') as filePath:
        currentLine = filePath.readline()
        while currentLine:
            element = currentLine.split(" ")[0]
            index = 0
            while index < len(element) and element[index] != '\'':
                index += 1

            element = element[index+1:]
            index = len(element) - 1
            while index >= 0 and element[index] != '\'':
                index -= 1
            element = element[:index]
            output.append(element)
            currentLine = filePath.readline()

    print(output)
    return output

parser = Parser("g1.txt")

#generateInputFromPIF("lab3/PIF.out")

parser.runAlgorithm(['a','a','c','b','c','a'])
#parser.runAlgorithm(["integer", "mainFunction", "(",  "epsilon", ")", "{", "epsilon", "epsilon", "}"])

#parser.runAlgorithm(generateInputFromPIF("lab3/PIF.out"))