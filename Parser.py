from Grammar import Grammar

class Parser:
    def __init__(self):
        self.currentState = 'q'
        self.index = 1
        self.workingStack = []
        self.inputStack = []
        self.grammar = Grammar("g1.txt")

    def expand(self):
        nonterminal = self.inputStack.pop(0)
        self.workingStack.append(nonterminal)
        self.inputStack.insert(0, self.grammar.productions[nonterminal])

    def advance(self):
        self.index += 1
        terminal = self.inputStack.pop(0)
        self.workingStack.append(terminal)

    def momentaryInsucces(self):
        self.currentState = 'b'

    def back(self):
        self.index -= 1
        lastFromWorkingStack = self. workingStack.pop()
        self.inputStack.insert(0, lastFromWorkingStack)

    def anotherTry(self):
        lastFromWorkingStack = self.workingStack.pop()
        checkIfNextExists = (lastFromWorkingStack[0], lastFromWorkingStack[1] + 1)
        if checkIfNextExists in self.grammar.productions:
            self.currentState = 'q'
            self.workingStack.append(checkIfNextExists)
        elif self.index == 1 and lastFromWorkingStack[0] == self.grammar.initialNonTerminal:
            raise Exception("ERROR")
        else:
            self.inputStack.insert(0, lastFromWorkingStack[0])

    def success(self):
        self.currentState = 'f'
        self.index += 1

    def runAlgorithm(self):
        #print(self.currentState)
        while self.currentState != "f" and self.currentState != "e":
            if self.currentState == "q":
                if self.inputStack.count() == 0 and self.index == self.grammar
