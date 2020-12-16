from lab3.HashTable import HashTable

def isSymbol(givenCharacter):
    if givenCharacter in "[]{}()!=*/\\;,<.>&|%":
        return True
    return False


class Scanner:
    def __init__(self, givenProgramFileName, givenTokensFileName):
        self.__programFileName = givenProgramFileName
        self.__tokensFileName = givenTokensFileName
        self.__tokensList = {}
        self.readAndCreateTokensList()
        self.__PIF = []
        self.__symbolTable = HashTable(100)

    def getPIF(self):
        return self.__PIF

    def readAndCreateTokensList(self):
        with open(self.__tokensFileName, 'r') as filePath:
            next(filePath)
            next(filePath)
            currentLine = filePath.readline()
            while currentLine:
                name, code = currentLine.split(" -> ")
                if code[-1] == '\n':
                    code = code[:-1]
                if name == "Space":
                    self.__tokensList[' '] = -1
                elif name == "identifier":
                    self.__tokensList[name] = 0
                elif name == "constant":
                    self.__tokensList[name] = "constant"
                else:
                    self.__tokensList[name] = -1

                currentLine = filePath.readline()

    def scanProgram(self, givenPIFFile="PIF.out", givenSymbolTableFile="ST.out"):
        with open(self.__programFileName, 'r') as filePath:
            lineNumber = 1
            currentLine = filePath.readline()
            if currentLine[-1] != '\n':
                currentLine = currentLine + '\n'
            index = 0
            while currentLine:
                currentElement = ""
                if currentLine[index].isalpha():
                    while currentLine[index] != '\n' and currentLine[index].isalpha():
                        currentElement += currentLine[index]
                        index += 1
                    if currentElement in self.__tokensList:
                        self.__PIF.append([currentElement, self.__tokensList[currentElement]])
                    else:
                        while currentLine[index] != '\n' and currentLine[index].isdigit():
                            currentElement += currentLine[index]
                            index += 1
                        if currentElement in self.__tokensList:
                            self.__PIF.append([currentElement, self.__tokensList[currentElement]])
                        elif self.__symbolTable.find(currentElement) == -1:
                            self.__symbolTable.add(currentElement)
                            self.__PIF.append(["identifier", self.__symbolTable.find(currentElement)])
                        else:
                            self.__PIF.append(["identifier", self.__symbolTable.find(currentElement)])

                elif currentLine[index].isdigit():
                    while currentLine[index] != '\n' and currentLine[index].isdigit():
                        currentElement += currentLine[index]
                        index += 1
                    if currentLine[index].isalpha():
                        # throw exception - invalid identifier
                        print(
                            "Lexical Error on line " + str(lineNumber) + ": Invalid identifier " + str(currentElement))
                        return
                    if len(currentElement) > 1 and currentElement[0] == '0':
                        # throw exception - number cannot start with 0
                        print("Lexical Error on line " + str(lineNumber) + ": Number cannot start with 0: "
                              + str(currentElement))
                        return

                    if self.__symbolTable.find(currentElement) == -1:
                        self.__symbolTable.add(currentElement)
                    self.__PIF.append(["constant", self.__symbolTable.find(currentElement)])

                elif currentLine[index] == '"':
                    currentElement += currentLine[index]
                    index += 1
                    while currentLine[index] != '\n' and currentLine[index] != '"' and currentLine[index] != '~':
                        currentElement += currentLine[index]
                        index += 1
                    if currentLine[index] == '\n':
                        # throw exception - invalid string
                        print("Lexical Error on line " + str(lineNumber) + ": Invalid string " +
                              str(currentElement) + "\"")
                        return
                    if currentLine[index] == '~':
                        # throw exception - invalid unfinished string
                        print("Lexical Error on line " + str(lineNumber) + ": Invalid unfinished string " +
                              str(currentElement) + "\"")
                        return

                    currentElement += currentLine[index]
                    index += 1
                    if self.__symbolTable.find(currentElement) == -1:
                        self.__symbolTable.add(currentElement)
                        self.__PIF.append(["constant", self.__symbolTable.find(currentElement)])
                    else:
                        self.__PIF.append(["constant", self.__symbolTable.find(currentElement)])

                elif currentLine[index] == '\'':
                    currentElement += currentLine[index]
                    index += 1
                    while currentLine[index] != '\n' and currentLine[index] != '\'':
                        currentElement += currentLine[index]
                        index += 1
                    if currentLine[index] == '\n':
                        # throw exception - invalid character
                        print("Lexical Error on line " + str(lineNumber) + ": Unfinished character declaration" +
                              str(currentElement) + '\'')
                        return
                    currentElement += currentLine[index]
                    index += 1
                    if len(currentElement) > 3:
                        # throw exception - invalid character
                        print("Lexical Error on line " + str(lineNumber) + ": Invalid character " +
                              str(currentElement) + '\'')
                        return
                    if self.__symbolTable.find(currentElement) == -1:
                        self.__symbolTable.add(currentElement)
                        self.__PIF.append(["constant", self.__symbolTable.find(currentElement)])
                    else:
                        self.__PIF.append(["constant", self.__symbolTable.find(currentElement)])

                elif currentLine[index] == ':':
                    currentElement += currentLine[index]
                    index += 1
                    while currentLine[index] != '\n' and currentLine[index] != ':':
                        currentElement += currentLine[index]
                        index += 1
                    if currentLine[index] == '\n':
                        # throw exception - : operator not finished
                        print("Lexical Error on line " + str(lineNumber) + ": Operator not finished (has to be of form "
                                                                           ":...:) : " + str(currentElement))
                        return
                    currentElement += currentLine[index]
                    index += 1
                    if currentElement not in self.__tokensList:
                        # throw exception: unkown/invalid operator
                        print("Lexical Error on line " + str(lineNumber) + ": Invalid/unknown operator " +
                              str(currentElement))
                        return
                    self.__PIF.append([currentElement, self.__tokensList[currentElement]])

                elif currentLine[index] == '~':
                    while currentLine[index] != '\n':
                        index += 1

                elif currentLine[index] == '-' or currentLine[index] == '+':
                    currentElement += currentLine[index]
                    index += 1
                    if self.__PIF[-1][0] == "constant":
                        constant = self.__symbolTable.getValueOfPosition(self.__PIF[-1][1])
                        if constant.isdigit() or constant[1:].isdigit():
                            self.__PIF.append([currentElement, self.__tokensList[currentElement]])

                    elif self.__PIF[-1][0] in "-+/%*" or currentLine[index].isdigit():
                        if currentLine[index].isdigit():
                            while currentLine[index] != '\n' and currentLine[index].isdigit():
                                currentElement += currentLine[index]
                                index += 1
                            if currentLine[index].isalpha():
                                # throw exception - invalid identifier
                                print(
                                    "Lexical Error on line " + str(lineNumber) + ": Invalid identifier " + str(
                                        currentElement))
                                return
                            if currentElement[1] == '0':
                                # throw exception - number cannot start with 0
                                print("Lexical Error on line " + str(lineNumber) + ": Number cannot start with 0/ we "
                                                                                   "cannot have -0 or +0: " + str(
                                                                                    currentElement))
                                return
                            if len(currentElement) == 1:
                                # throw exception - we have a - or + without any number after it
                                print("Lexical Error on line " + str(lineNumber) + ": We have a + or a - without any "
                                                                                   "number after it: " + str(
                                                                                    currentElement))
                                return
                            if self.__symbolTable.find(currentElement) == -1:
                                self.__symbolTable.add(currentElement)
                                self.__PIF.append(["constant", self.__symbolTable.find(currentElement)])
                            else:
                                self.__PIF.append(["constant", self.__symbolTable.find(currentElement)])

                        else:
                            self.__PIF.append([currentElement, self.__tokensList[currentElement]])

                    else:
                        self.__PIF.append([currentElement, self.__tokensList[currentElement]])

                elif isSymbol(currentLine[index]):
                    while currentLine[index] != '\n' and isSymbol(currentLine[index]):
                        currentElement += currentLine[index]
                        index += 1
                        if currentElement in self.__tokensList:
                            self.__PIF.append([currentElement, self.__tokensList[currentElement]])
                            break
                    if currentElement not in self.__tokensList:
                        # throw exception: unknown symbol/combination of symbols
                        print("Lexical Error on line" + str(lineNumber) + ": Unknown symbol/combination of symbols "
                              + str(currentElement))
                        return
                elif currentLine[index] == ' ' or currentLine[index] == '\t':
                    index += 1
                else:
                    print("Lexical Error on line " + str(lineNumber) + ": Unknown symbol " + str(currentLine[index]))
                    return
                if index >= len(currentLine) or currentLine[index] == '\n':
                    currentLine = filePath.readline()
                    index = 0
                    lineNumber += 1
        print("Lexically correct")
        self.printPIF(givenPIFFile)
        self.printSymbolTable(givenSymbolTableFile)

    def printPIF(self, givenPIFFile):
        with open(givenPIFFile, 'w') as filePath:
            for element in self.__PIF:
                filePath.write(str(element) + '\n')

    def printSymbolTable(self, givenSymbolTableFile):
        with open(givenSymbolTableFile, 'w') as filePath:
            filePath.write(
                "Symbol Table created using a Hash Map, collision resolution similar to coalesced chaining\n")
            filePath.write(self.__symbolTable.printString())

