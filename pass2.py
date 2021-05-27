import re
from typing import final
import ToolsFile
import pass1

with open("instructions.txt") as textFile:
    opArr = [line.split(' ') for line in textFile]
with open("symbolTable.txt") as textFile:
    symbArr = [line.split(' ') for line in textFile]

finalArr = ToolsFile.appendall()

objectcodeFile = open("ObjectCode.txt", "wt")

LFile = open("locationCounter.txt", "rt")
LArray = LFile.readlines()


def ObjectCode():

    for i in range(len(finalArr)):  # Tracing the first row of our list.

        if "BYTE" in finalArr[i][1]:
            # Byte have two cases: either ASCII of characters or their immediate value.
            if "C'" in finalArr[i][2]:
                pureChars = finalArr[i][2][2:].replace("'", '')
                # ORD function helps convert characters to ASCII values
                # We used it then stored the value on the Object Code table
                addressBits = ''.join(hex(ord(C)).split(
                    'x')[-1].upper() for C in pureChars)
                # We write down the Object Code
                objectcodeFile.write(addressBits+"\n")
            if "X'" in finalArr[i][2]:
                addressBits = finalArr[i][2][2:].replace("'", '')
                # We write down the Object Code
                objectcodeFile.write(addressBits+"\n")

        # We check if we are reading the operations that shouldn't generate Object Code.
        if "RESW" in finalArr[i][1] or "RESB" in finalArr[i][1] or "RESTW" in finalArr[i][1] or "RESDW" in finalArr[i][1] or "EQU" in finalArr[i][1] or "BASE" in finalArr[i][1] or "LTORG" in finalArr[i][1] or "END" in finalArr[i][1]:
            opBits = "No object code!"
            objectcodeFile.write(opBits+"\n")

        # Starting from here if we have the cases of WORD or BYTE, we do a specific calculation.
        if "WORD" in finalArr[i][1]:
            # We used .split('x')[-1].upper() to neglect the 0X
            # that's in our result then capitalize it.
            addressBits = hex(int(finalArr[i][2])).split('x')[-1].upper()
            objectcodeFile.write(addressBits.zfill(6)+"\n")

        # If we passed by an RSUB
        if "RSUB" in finalArr[i][1]:
            objectcodeFile.write("4C0000"+"\n")

        # If the operation is a lateral
        if '=' in finalArr[i][1]:
            # Byte have two cases: either ASCII of characters or their immediate value.
            if "C'" in finalArr[i][1]:
                pureChars = finalArr[i][1][2:].replace("'", '')
                # ORD function helps convert characters to ASCII values
                # We used it then stored the value on the Object Code table
                addressBits = ''.join(hex(ord(C)).split(
                    'x')[-1].upper() for C in pureChars)
                # We write down the Object Code
                objectcodeFile.write(addressBits+"\n")
            if "X'" in finalArr[i][1]:
                addressBits = finalArr[i][1][2:].replace("'", '')
                # We write down the Object Code
                objectcodeFile.write(addressBits+"\n")

        else:

            if ToolsFile.checkformat(finalArr[i][1]) == '1':
                opBits = ToolsFile.getOpCode(finalArr[i][1])
                objectcodeFile.write(opBits+"\n")

            elif ToolsFile.checkformat(finalArr[i][1]) == '2':
                opBits = ToolsFile.getOpCode(finalArr[i][1]).replace("\n", '')
                if ',' in finalArr[i][2]:
                    regs = finalArr[i][2].split(',')
                    r1 = str(ToolsFile.GetRegister(regs[0]))
                    r2 = str(ToolsFile.GetRegister(regs[1]))
                else:
                    r1 = str(ToolsFile.GetRegister(finalArr[i][2]))
                    r2 = '0'
                objectcodeFile.write(opBits+r1+r2 + "\n")

    objectcodeFile.close()
