import re
# The toolsFile program is used as external tool for usage in pass 1 & 2


# We read the assembly program from the user in program.txt
# testprogram is for other uses not related to the user
fin = open("testprogram.txt", "rt")
fout = open("program.txt", "wt")
for line in fin:
    # We put a '*' after each line of assembly code
    fout.write(re.sub('\s+', '_', line))
    fout.write('\n')

fin.close()
fout.close()

with open("program.txt") as textFile:
    progArr = [line.split('_') for line in textFile]
with open("instructions.txt") as textFile:
    instructions = [line.split(' ') for line in textFile]
with open("symbolTable.txt") as textFile:
    symbols = [line.split(' ') for line in textFile]
with open("literalTable.txt") as textFile:
    literals = [line.split(' ') for line in textFile]

# To check the instructions for the unique. #
# ones and the one in the instruction text. #

# To get the last number of the location counter
locationFile = open("locationCounter.txt", "rt")
locationCounter = locationFile.readlines()


# Used as a checker if there's an undefined instruction
def checkinstructions(teststring):
    i = 0
    found = False
    if teststring in "RESB":
        found = True
    if teststring in "BYTE":
        found = True
    if teststring in "WORD":
        found = True
    if teststring in "RESW":
        found = True
    if teststring in "RESTW":
        found = True
    if teststring in "RESDW":
        found = True
    if teststring in "BASE":
        found = True
    if teststring in "LTORG":
        found = True
    if teststring in "EQU":
        found = True
    if teststring in "RSUB":
        found = True
    if "=" in teststring:
        found = True
    if "END" in teststring:
        found = True
    while i in range(len(instructions)):
        if instructions[i][0] in teststring:
            found = True
        i = i + 1
    return found


# This function will check if there's a comment
# in the OPERATIONS, and if there is we created a new
# array to store the instructions that don't
# start with a comment
def operations():
    opArray = []
    for i in range(1, len(progArr)):  # We start from the row after start
        if checkinstructions(progArr[i][1]) == True:
            opArray.append(progArr[i][1])
        elif ('.' in progArr[i][2]) or ('.' in progArr[i][1]) or ('.' in progArr[i][0]):
            opArray.append(progArr[i][1])
        else:
            print("ERROR: Wrong instruction input.")
            break
    return opArray


# This function will check if there's a comment
# in the VARIABLES, and if there is we created a new
# array to store the instructions that don't
# start with a comment
def variables():
    varArray = []
    for i in range(1, len(progArr)):  # We start from the row
        varArray.append(progArr[i][2])
    return varArray


# This function will check if there's a comment
# in the INDEXES, and if there is we created a new
# array to store the instructions that don't
# start with a comment
def indexs():
    indexsArray = []
    for i in range(1, len(progArr)):  # We start from the row
        indexsArray.append(progArr[i][0])
    return indexsArray


# We take all the lists of indexes, operations and
# variables and store them in the array the program
# will execute on.
def appendall():
    finalArray = []
    finalArray = list(zip(indexs(), operations(), variables()))
    return finalArray
# function to get the starting address of the program


# To get the value of the start of the program
def startingadress():
    startlocation = progArr[0][2]
    return startlocation

# To get the name of the program


def ProgName():
    ProgName = progArr[0][0].ljust(6, 'x')
    # print(ProgName)
    return ProgName


def ProgLength():
    ProgLen = hex(int(locationCounter[-1], 16) +
                  1).split('x')[-1].upper().zfill(6)
    # print(ProgLen)
    return ProgLen


def checkformat(teststring1):
    for i in range(len(instructions)):
        if instructions[i][0] in teststring1:

            return instructions[i][1]


def getOpCode(teststring1):
    for i in range(len(instructions)):
        if instructions[i][0] in teststring1:
            return instructions[i][2]


# Used to find the split of the arithematic operation of the addresses
def handlEQU(var):

    finalArray = appendall()
    for i in range(len(finalArray)):
        if var in finalArray[i][0]:
            wanted = i

    return wanted


def GetRegister(var):

    if 'A' in var:
        return 0
    if 'X' in var:
        return 1
    if 'L' in var:
        return 2
    if 'B' in var:
        return 3
    if 'S' in var:
        return 4
    if 'T' in var:
        return 5
    if 'F' in var:
        return 6


def findAddress(mystring):  # method to search for the address in the symbol table
    if '=' in mystring:
        for i in range(len(literals)):
            if literals[i][0] in mystring:
                return literals[i][2].replace("\n", '')
                break
    else:
        for i in range(len(symbols)):
            if symbols[i][0] in mystring:
                return symbols[i][1].replace("\n", '')
                break


def findpc(myindex):  # method to find the pc
    for i in range(len(locationCounter)):
        if myindex == i:  # law ana wa2ef 3and element rakam i
            if "-----" in locationCounter[i+1]:
                return locationCounter[i+2].replace("\n", '')
                break
            else:
                return locationCounter[i+1].replace("\n", '')
                break


def findBase():  # method to search for the address in the symbol table
    finArr = appendall()
    for i in range(len(finArr)):
        if 'BASE' in finArr[i][1]:
            baseVar = finArr[i][2]
    for i in range(len(symbols)):
        if symbols[i][0] in baseVar:
            return symbols[i][1].replace("\n", '')
