import re
import ToolsFile


def locationCounter():
    # A split array to store the location counter for the special conditions like equ
    currentCounterArr = []
    counter = hex(int(ToolsFile.startingadress())).split(
        'x')[-1].upper()  # Store the beginning of the counter
    fout = open("locationCounter.txt", "wt")
    # The whole program in the finalArray
    finalArray = ToolsFile.appendall()
    # print(finalArray)
    temp = int(counter, 16)  # we turn hex to int to be able to count

    for i in range(len(finalArray)):

        currentCounterArr.append(temp)
        # If there's a comment we skip the line, no location or any calculation counted
        if ('.' in finalArray[i][2]) or ('.' in finalArray[i][1]) or ('.' in finalArray[i][0]):
            fout.write('-----')
            fout.write('\n')

        # Same with the other cases below
        elif ('BASE' in finalArray[i][1]) or ('LTORG' in finalArray[i][1]) or ('END' in finalArray[i][1]):
            fout.write('-----')
            fout.write('\n')

        # If EQU case, we don't location count
        elif 'EQU' in finalArray[i][1]:
            temp = temp + 0
            # Print the location counter of the previous normally
            if '*' in finalArray[i][2]:
                counter = hex(temp).split('x')[-1].upper()
                fout.write(str(counter).zfill(4))
                fout.write('\n')

            # The next 4 elif conditions are arithematic operations
            elif ('-' in finalArray[i][2]):
                # Split the two variables (ex: buffend-buffer) and store them alone
                variables = finalArray[i][2].split('-')
                # If the variable is a number
                if variables[0].isdigit():
                    var1 = int(variables[0])
                # If the variable is an address
                else:
                    var1 = currentCounterArr[ToolsFile.handlEQU(variables[0])]
                if variables[1].isdigit():
                    var2 = int(variables[1])
                else:
                    var2 = currentCounterArr[ToolsFile.handlEQU(variables[1])]

                # Print with the operation done
                fout.write(str(hex(var1-var2).split('x')[-1].upper()).zfill(4))
                fout.write('\n')

            elif ('+' in finalArray[i][2]):
                variables = finalArray[i][2].split('+')
                if variables[0].isdigit():
                    var1 = int(variables[0])
                else:
                    var1 = currentCounterArr[ToolsFile.handlEQU(variables[0])]
                if variables[1].isdigit():
                    var2 = int(variables[1])
                else:
                    var2 = currentCounterArr[ToolsFile.handlEQU(variables[1])]
                fout.write(str(hex(var1+var2).split('x')[-1].upper()).zfill(4))
                fout.write('\n')

            elif ('*' in finalArray[i][2]):
                variables = finalArray[i][2].split('*')
                if variables[0].isdigit():
                    var1 = int(variables[0])
                else:
                    var1 = currentCounterArr[ToolsFile.handlEQU(variables[0])]
                if variables[1].isdigit():
                    var2 = int(variables[1])
                else:
                    var2 = currentCounterArr[ToolsFile.handlEQU(variables[1])]
                fout.write(str(hex(var1*var2).split('x')[-1].upper()).zfill(4))
                fout.write('\n')

            elif ('/' in finalArray[i][2]):
                variables = finalArray[i][2].split('/')
                if variables[0].isdigit():
                    var1 = int(variables[0])
                else:
                    var1 = currentCounterArr[ToolsFile.handlEQU(variables[0])]
                if variables[1].isdigit():
                    var2 = int(variables[1])
                else:
                    var2 = currentCounterArr[ToolsFile.handlEQU(variables[1])]
                fout.write(str(hex(var1/var2).split('x')[-1].upper()).zfill(4))
                fout.write('\n')

        # The normal case
        else:

            counter = hex(temp).split('x')[-1].upper()
            fout.write(str(counter).zfill(4))
            fout.write('\n')

        # we calculate the odd cases for their specific calculations
        if 'BYTE' in finalArray[i][1]:
            temp = temp + 1
        # If of the 3 cases
        elif ('BASE' in finalArray[i][1]) or ('LTORG' in finalArray[i][1]) or ('END' in finalArray[i][1]):
            temp = temp + 0
        # If it's a comment–we added it because we found it countering during comments.
        elif ('.' in finalArray[i][0]) or ('.' in finalArray[i][1]) or ('.' in finalArray[i][2]):
            temp = temp + 0

        elif 'RESB' in finalArray[i][1]:
            temp = temp + int(finalArray[i][2])
        elif 'RESW' in finalArray[i][1]:
            temp = temp + (int(finalArray[i][2])) * 3
        elif 'RESTW' in finalArray[i][1]:
            temp = temp + ((int(finalArray[i][2])) * 3) * 3
        elif 'RESDW' in finalArray[i][1]:
            temp = temp + ((int(finalArray[i][2])) * 3) * 2

        # If it's a lateral
        elif '=' in finalArray[i][1]:
            # Gets what's inside the C'_'
            temp = temp + len(finalArray[i][1][3:].replace("'", ''))

        # A normal function and check it's format
        else:
            if ToolsFile.checkformat(finalArray[i][1]) == '1':
                temp = temp + 1
            elif ToolsFile.checkformat(finalArray[i][1]) == '2':
                temp = temp + 2
            elif ToolsFile.checkformat(finalArray[i][1]) == '34':
                if '+' in finalArray[i][1]:
                    temp = temp + 4
                else:
                    temp = temp + 3
            else:
                temp = temp + 0


def SymbolTable():
    fout = open("locationCounter.txt", "rt")
    fout2 = open("symbolTable.txt.", "wt")

    # we initiate a variable with the final array we made before that has the program
    finalArray = ToolsFile.appendall()
    # we put the location counter we made in a variable as well
    locationArray = fout.readlines()
    for i in range(len(finalArray)):
        # if we don't have an index in the first column then we skip it
        if (finalArray[i][0] != '') and (finalArray[i][0] != '*') and ('.' not in finalArray[i][0]) and ('.' not in finalArray[i][1]) and ('.' not in finalArray[i][2]):
            symbol1 = finalArray[i][0]  # we write the index
            # then put beside it the calculated location of it
            symbol2 = locationArray[i]
            fout2.write(symbol1 + ' ' + symbol2)


def literalTable():
    fout = open("locationCounter.txt", "rt")
    fout2 = open("literalTable.txt.", "wt")

    # we initiate a variable with the final array we made before that has the program
    finalArray = ToolsFile.appendall()
    # we put the location counter we made in a variable as well
    locationArray = fout.readlines()
    for i in range(len(finalArray)):
        # if we don't have an index in the first column then we skip it
        if '*' in finalArray[i][0]:
            symbol1 = finalArray[i][1].replace('=', '')  # we write the index
            # then put beside it the calculated location of it
            symbol2 = locationArray[i]
            if 'C' in finalArray[i][1]:
                pureChars = finalArray[i][1][3:].replace("'", '')
                symbol3 = ''.join(hex(ord(C)).split(
                    'x')[-1].upper() for C in pureChars)
            elif 'X' in finalArray[i][1]:
                pureChars = finalArray[i][1][3:].replace("'", '')
                symbol3 = pureChars
            fout2.write(symbol1 + ' ' + symbol3 + ' ' + symbol2)