from Parser import Parser
from Grammar import Grammar

grammar = Grammar("g2.txt")

grammar.printAll()

#grammar.printOneNonTerminal()

parser = Parser()

parser.runAlgorithm()