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


def getMrecord():
    Marr = []
    for i in range(len(finalArr)):
        if '+' in finalArr[i][1]:
            if '#' in finalArr[i][2] and finalArr[i][2].replace('#', '').isdigit():
                pass  # Skips the immediate case
            else:  # If it's a normal format 4 case
                wantedLocation = hex(
                    int(LArray[i], 16)+1).split('x')[-1].upper()
                wantedLocationStr = str(wantedLocation).zfill(6)
                Marr.append('M.'+wantedLocationStr+'.05')
    return Marr


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
        elif "EQU" in finalArr[i][1] or "BASE" in finalArr[i][1] or "LTORG" in finalArr[i][1] or "END" in finalArr[i][1]:
            opBits = "---"
            objectcodeFile.write(opBits+"\n")
        elif "RESW" in finalArr[i][1] or "RESB" in finalArr[i][1] or "RESTW" in finalArr[i][1] or "RESDW" in finalArr[i][1]:
            opBits = "No object code!"
            objectcodeFile.write(opBits+"\n")
        # Starting from here if we have the cases of WORD or BYTE, we do a specific calculation.
        elif "WORD" in finalArr[i][1]:
            # We used .split('x')[-1].upper() to neglect the 0X
            # that's in our result then capitalize it.
            addressBits = hex(int(finalArr[i][2])).split('x')[-1].upper()
            objectcodeFile.write(addressBits.zfill(6)+"\n")

        # If we passed by an RSUB
        elif "RSUB" in finalArr[i][1]:
            objectcodeFile.write("4F0000"+"\n")
        elif '.' in finalArr[i][0] or '.' in finalArr[i][1] or '.' in finalArr[i][2]:
            opBits = "---"
            objectcodeFile.write(opBits + "\n")
        # If the operation is a lateral
        elif '=' in finalArr[i][1]:
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

        # Since none of the special cases, we'll see which format
        else:

            # Format 1
            if ToolsFile.checkformat(finalArr[i][1]) == '1':
                # Put the Opcode and write it in the object code
                opBits = ToolsFile.getOpCode(finalArr[i][1])
                objectcodeFile.write(opBits+"\n")

            # Format 2
            elif ToolsFile.checkformat(finalArr[i][1]) == '2':
                # Opcode
                # We put .replace to make sure it doesn't take the \n with it
                opBits = ToolsFile.getOpCode(finalArr[i][1]).replace("\n", '')
                # Registers
                # If there are two registers, else just r1 register
                if ',' in finalArr[i][2]:
                    regs = finalArr[i][2].split(',')
                    r1 = str(ToolsFile.GetRegister(regs[0]))
                    r2 = str(ToolsFile.GetRegister(regs[1]))
                else:
                    r1 = str(ToolsFile.GetRegister(finalArr[i][2]))
                    r2 = '0'
                objectcodeFile.write(opBits+r1+r2 + "\n")

            # Format 3 & 4 & Q
            elif ToolsFile.checkformat(finalArr[i][1]) == '34':
                opHex = ToolsFile.getOpCode(finalArr[i][1].replace("\n", ''))
                opInt = int(opHex, 16)
                opBin = str(bin(opInt))[2:].zfill(8)  # 2: to drop the 0B
                opBits = opBin[0:6]  # drop first 2 bits
                # The 4 lines above are for converting the Opcode from hex to binary for calculation

                if '#' in finalArr[i][2]:  # we sit the n-i if it has immediate
                    niBits = '01'
                elif '@' in finalArr[i][2]:  # same if it has indirect
                    niBits = '10'
                else:  # the default case
                    niBits = '11'
                # So far we got op-code and n-i

                # If there's an x-bit
                if ',X' in finalArr[i][2]:
                    xBits = '1'
                else:
                    xBits = '0'

                # Now we set the b-p, starting with the format 4 or immediate case
                if '+' in finalArr[i][1] or finalArr[i][2].replace('#', '').isdigit():
                    bpBits = '00'
                else:  # default case/format 3
                    bpBits = '01'

                # We have op-code, n-i, x, b-p, what's left is e
                if '+' in finalArr[i][1]:  # if it's a format 4, e=1
                    eBits = '1'
                else:  # format 3
                    eBits = '0'

                # We have everything, only address/displacement left
                if '+' in finalArr[i][1]:  # if format 4
                    # Get the address of the variable column whether symbol table or literal table
                    wholeAddressStr = ToolsFile.findAddress(
                        finalArr[i][2]).zfill(5)  # To make sure it's in 20 bits
                elif '&' in finalArr[i][1]:  # The Q format case
                    niBits = '00'
                    eBits = '0'
                    firstAddress = ToolsFile.findAddress(  # Searches in the symbol table
                        finalArr[i][2])
                    secondAddress = ToolsFile.findpc(i)  # Gets the PC counter
                    # The displacement calculation
                    QWholeAddress = int(firstAddress, 16) - \
                        int(secondAddress, 16)
                    # Q-format's flags' conditions
                    if QWholeAddress == 0:
                        eBits = 1
                    if QWholeAddress < 0 and (QWholeAddress % 2) == 1:
                        niBits = '11'
                    elif QWholeAddress < 0 and (QWholeAddress % 2) == 0:
                        niBits = '01'
                    elif QWholeAddress > 0 and (QWholeAddress % 2) == 1:
                        niBits = '10'
                    else:
                        niBits = '00'
                    wholeAddress = hex(QWholeAddress & (
                        2**20-1)).split('x')[-1].upper()
                    wholeAddress = wholeAddress[-3:]
                    wholeAddressStr = str(wholeAddress).zfill(3)

                else:  # Format 3
                    if '#' in finalArr[i][2]:  # If it's immediate & digit ex: #4096
                        if finalArr[i][2].replace('#', '').isdigit():
                            immediate = finalArr[i][2].replace('#', '')
                            wholeAddressStr = immediate.zfill(3)
                    else:  # We calculate the displacement
                        firstAddress = ToolsFile.findAddress(  # Searches in the symbol table
                            finalArr[i][2])
                        secondAddress = ToolsFile.findpc(
                            i)  # gets the PC counter
                        # The displacement calculation
                        wholeAddress = hex(
                            int(firstAddress, 16)-int(secondAddress, 16)).split('x')[-1].upper()
                        if len(wholeAddress) > 3:  # The out of range case
                            bpBits = '10'  # b & p will be 1 0 since it's out of range
                            secondAddress = ToolsFile.findBase()  # Recalculates with the base
                        wholeAddress = hex((
                            int(firstAddress, 16)-int(secondAddress, 16)) & (2**20-1)).split('x')[-1].upper()
                        wholeAddress = wholeAddress[-3:]
                        wholeAddressStr = str(wholeAddress).zfill(3)
                # The object code assembly
                part1objBin = (opBits+''+niBits+''+xBits+''+bpBits+''+eBits)
                part1objInt = (int(part1objBin, 2))  # Turn it to int
                part1objhex = hex(part1objInt).split(  # Then hex
                    'x')[-1].upper().zfill(3)
                # Stored in the object code file
                objectcodeFile.write(part1objhex+''+wholeAddressStr+'\n')

    objectcodeFile.close()


def HTME_Record():

    # HTE Record storation
    open('HTE_Record.txt', 'w').close()

    # We assigned lists from the object code for the HTE
    HTE_File = open("HTE_Record.txt", "a")
    ObjectFile = open("ObjectCode.txt", "rt")
    ObjectCodeArray = ObjectFile.readlines()
    # To get the header (H.)
    Header = str("H." + ToolsFile.ProgName() + "." +
                 ToolsFile.startingadress().zfill(6) + "." + ToolsFile.ProgLength())
    HTE_File.write(Header+"\n")
    # to get the m record
    Modification = getMrecord()
    # To get the end (E.)
    End = str("E." + ToolsFile.startingadress().zfill(6))

    # assigned our initiatives for the loop below
    Count = 0
    TStart = ToolsFile.startingadress()
    Tobj = ""  # A temp that carries T record

    # To get the text (T.)
    for i in range(len(ObjectCodeArray)):  # We loop through the Object Code file
        # The break condition of the Text record
        if ("No object code!" in ObjectCodeArray[i]):
            if Tobj != "":  # As long as Tobj doesn't equal to ""
                HTE_File.write(hex(Count).split(  # Stores length of the t-record
                    'x')[-1].upper().zfill(2)+""+str(Tobj).replace("\n", "")+"\n")
            Count = 0
            Tobj = ""
        elif ("---" in ObjectCodeArray[i]):
            pass
        elif (Count >= 27):  # The other break condition of the Text record
            # We put it due to a bug not properly executing the lines below
            if Tobj != "" and '-----' not in LArray[i]:
                HTE_File.write(hex(Count).split(
                    'x')[-1].upper().zfill(2)+""+str(Tobj).replace("\n", "")+"\n")
            # RELATED: we put the counter to 3 because we used a word in the T record
                # subtracted 1 for range out of bound & divided by 2 because one hex is two bytes
                Count = int((len(ObjectCodeArray[i]) - 1) / 2)
                HTE_File.write(
                    "T." + LArray[i].zfill(6).replace("\n", "") + ".")
                Tobj = ("."+ObjectCodeArray[i])
            elif Tobj != "" and '-----' in LArray[i]:
                # we wouldn't be able to execute the others below and make a new T-record
                HTE_File.write(hex(Count).split(
                    'x')[-1].upper().zfill(2)+""+str(Tobj).replace("\n", "")+"\n")
                Count = int((len(ObjectCodeArray[i]) - 1) / 2)
                HTE_File.write(
                    "T." + LArray[i+1].zfill(6).replace("\n", "") + ".")
                Tobj = ("."+ObjectCodeArray[i])

        elif i == len(ObjectCodeArray)-1:  # When the text record reaches the end
            Tobj = (Tobj+"."+ObjectCodeArray[i])
            if Tobj != "":
                HTE_File.write(hex(Count).split(
                    'x')[-1].upper().zfill(2) + "" + str(Tobj).replace("\n", "") + "\n")
            for i in range(len(Modification)):
                HTE_File.write(Modification[i]+"\n")
            HTE_File.write(End)
        else:
            # RELATED: the reason why we made the count = 3 above was
            if Count == 0 and '-----' not in LArray[i]:
                # we wouldn't be able to execute the others below and make a new T-record
                HTE_File.write(
                    "T." + LArray[i].zfill(6).replace("\n", "") + ".")
            # RELATED: the reason why we made the count = 3 above was
            elif Count == 0 and '-----' in LArray[i]:
                # we wouldn't be able to execute the others below and make a new T-record
                HTE_File.write(
                    "T." + LArray[i+1].zfill(6).replace("\n", "") + ".")
            Count = Count+int((len(ObjectCodeArray[i]) - 1) / 2)
            Tobj = (Tobj+"."+ObjectCodeArray[i])

    HTE_File.close()
