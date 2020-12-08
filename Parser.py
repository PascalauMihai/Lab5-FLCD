from Grammar import Grammar


class Parser:
    def __init__(self):
        self.currentState = 'q'
        self.index = 0
        self.workingStack = []
        self.grammar = Grammar("g1.txt")
        self.debug = True
        self.inputStack = [(self.grammar.getInitialNonTerminal(), 1)]

    def printParserStep(self):
        print("~~~~~~~~~~~~")
        print(self.currentState)
        print(self.index)
        print("working stack: " + str(self.workingStack))
        print("input stack: " + str(self.inputStack))

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
        if self.debug:
            self.printParserStep()

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
        if self.debug:
            self.printParserStep()

    def momentaryInsucces(self):
        self.currentState = 'b'
        if self.debug:
            self.printParserStep()

    def back(self):
        self.index -= 1
        lastFromWorkingStack = [self.workingStack.pop()]
        self.inputStack.insert(0, lastFromWorkingStack)
        if self.debug:
            self.printParserStep()

    def anotherTry(self):
        if self.debug:
            self.printParserStep()
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
        if self.debug:
            self.printParserStep()

    def checkWordLenght(self, w):
        if len(w) > self.index: return self.inputStack[0][0] == w[self.index]
        return False

    def runAlgorithm(self, w):
        if self.debug:
            self.printParserStep()

        while self.currentState != "f" and self.currentState != "e":
            if self.currentState == "q":
                if len(self.inputStack) == 0 and self.index == len(w):
                    self.currentState = "f"
                else:
                    if self.inputStack[0][0] in self.grammar.getNonTerminals():
                        self.expand()
                    elif self.inputStack[0][0] in self.grammar.getTerminals() and self.checkWordLenght(w):
                        self.advance()
                    else:
                        self.momentaryInsucces()
            elif self.currentState == "b":
                if self.workingStack[-1] in self.grammar.getTerminals():
                    self.back()
                else:
                    self.anotherTry()
                    if self.debug:
                        self.printParserStep()
        if self.currentState == "e":
            print("!!!!!!!!!!!!! EROARE !!!!!!!!!!!!!")
        else:
            print("WE GOOOOOOOOOOOOOOOOOOOOOOO")
            print(self.workingStack)


parser = Parser()

parser.runAlgorithm(['a','a','c','b','c'])