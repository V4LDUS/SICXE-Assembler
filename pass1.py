import re
import ToolsFile

def locationCounter():
    # Starting address from ToolsFile, we put the first value in counter variable
    currentCounterArr = []
    counter = hex(int(ToolsFile.startingadress())).split('x')[-1].upper()
    fout = open("locationCounter.txt", "wt")  # print the start
    # padding the number to be written in 4 bits
    finalArray = ToolsFile.appendall()
    print(finalArray)
    temp = int(counter, 16)  # we turn hex to int to be able to count
    for i in range(len(finalArray)):
        currentCounterArr.append(temp)
        if ('.' in finalArray[i][2]) or ('.' in finalArray[i][1]) or ('.' in finalArray[i][0]):
            fout.write('-----')
            fout.write('\n')
        elif ('BASE' in finalArray[i][1]) or ('LTORG' in finalArray[i][1]) or ('END' in finalArray[i][1]):
            fout.write('-----')
            fout.write('\n')
        elif 'EQU' in finalArray[i][1]:
            temp = temp + 0
            if '*' in finalArray[i][2]:
                counter = hex(temp).split('x')[-1].upper()
                fout.write(str(counter).zfill(4))
                fout.write('\n')
            elif ('-' in finalArray[i][2]) :
                variables = finalArray[i][2].split('-')
                if variables[0].isdigit() :
                    var1=int(variables[0])
                else :
                    var1=currentCounterArr[ToolsFile.handlEQU(variables[0])]
                if variables[1].isdigit() :
                    var2=int(variables[1])
                else:
                    var2=currentCounterArr[ToolsFile.handlEQU(variables[1])]
                fout.write(str(hex(var1-var2).split('x')[-1].upper()).zfill(4))
                fout.write('\n')
            elif ('+' in finalArray[i][2]) :
                variables = finalArray[i][2].split('+')
                if variables[0].isdigit() :
                    var1=int(variables[0])
                else :
                    var1=currentCounterArr[ToolsFile.handlEQU(variables[0])]
                if variables[1].isdigit() :
                    var2=int(variables[1])
                else:
                    var2=currentCounterArr[ToolsFile.handlEQU(variables[1])]
                fout.write(str(hex(var1+var2).split('x')[-1].upper()).zfill(4))
                fout.write('\n')
            elif ('*' in finalArray[i][2]) :
                variables = finalArray[i][2].split('*')
                if variables[0].isdigit() :
                    var1=int(variables[0])
                else :
                    var1=currentCounterArr[ToolsFile.handlEQU(variables[0])]
                if variables[1].isdigit() :
                    var2=int(variables[1])
                else:
                    var2=currentCounterArr[ToolsFile.handlEQU(variables[1])]
                fout.write(str(hex(var1*var2).split('x')[-1].upper()).zfill(4))
                fout.write('\n')
            elif ('/' in finalArray[i][2]) :
                variables = finalArray[i][2].split('/')
                if variables[0].isdigit() :
                    var1=int(variables[0])
                else :
                    var1=currentCounterArr[ToolsFile.handlEQU(variables[0])]
                if variables[1].isdigit() :
                    var2=int(variables[1])
                else:
                    var2=currentCounterArr[ToolsFile.handlEQU(variables[1])]
                fout.write(str(hex(var1/var2).split('x')[-1].upper()).zfill(4))
                fout.write('\n')


        else:

            counter = hex(temp).split('x')[-1].upper()
            fout.write(str(counter).zfill(4))
            fout.write('\n')
        # we calculate the odd cases for their specific calculations
        if 'BYTE' in finalArray[i][1]:
            temp = temp + 1
        elif ('BASE' in finalArray[i][1]) or ('LTORG' in finalArray[i][1]) or ('END' in finalArray[i][1]):
            temp = temp + 0
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
        elif '=' in finalArray[i][1]:
            temp = temp + len(finalArray[i][1][3:].replace("'", ''))
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
        if (finalArray[i][0] != '') or (finalArray[i][0] != '*'):  # if we don't have an index in the first column then we skip it
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
        if '*' in finalArray[i][0]:  # if we don't have an index in the first column then we skip it
            symbol1 = finalArray[i][1].replace('=','')  # we write the index
            # then put beside it the calculated location of it
            symbol2 = locationArray[i]
            if 'C' in finalArray[i][1]:
                pureChars = finalArray[i][1][3:].replace("'", '')
                symbol3 =''.join(hex(ord(C)).split('x')[-1].upper() for C in pureChars)
            elif 'X'in finalArray[i][1]:
                pureChars = finalArray[i][1][3:].replace("'", '')
                symbol3 = pureChars
            fout2.write(symbol1 + ' ' +symbol3+ ' ' + symbol2)