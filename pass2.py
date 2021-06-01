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
    Marr=[]
    for i in range(len(finalArr)):
        if '+' in finalArr[i][1] :
            if '#' in finalArr[i][2] and finalArr[i][2].replace('#','').isdigit():
                pass
                #just skip the immediate
            else : #law case 3adeya lel m record
                wantedLocation=hex(int(LArray[i],16)+1).split('x')[-1].upper()
                wantedLocationStr=str(wantedLocation).zfill(6)
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
        elif "RESW" in finalArr[i][1] or "RESB" in finalArr[i][1] or "RESTW" in finalArr[i][1] or "RESDW" in finalArr[i][1] or "EQU" in finalArr[i][1] or "BASE" in finalArr[i][1] or "LTORG" in finalArr[i][1] or "END" in finalArr[i][1]:
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
            objectcodeFile.write("4C0000"+"\n")

        # If the operation is a lateral
        elif '=' in finalArr[i][1]:
            # Byte have two cases: either ASCII of characters or their immediate value.
            if "C'" in finalArr[i][1]:
                pureChars = finalArr[i][1][2:].replace("'", '')
                # ORD function helps convert characters to ASCII values
                # We used it then stored the value on the Object Code table
                addressBits = ''.join(hex(ord(C)).split('x')[-1].upper() for C in pureChars)
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
            elif ToolsFile.checkformat(finalArr[i][1]) == '34': # if format 3 or 4 hangeeb kol 7aga m3ada el address delwa2ty
                opHex = ToolsFile.getOpCode(finalArr[i][1].replace("\n", ''))
                opInt= int(opHex,16) #convert the opcode to int so we can get it in binary
                opBin = str(bin(opInt))[2:].zfill(8) #get it in binary
                opBits = opBin[0:6] #sa2at a5er 2 bits
                # hanroo7 neshoof el ni bits
                if '#' in finalArr[i][2] : #Law imm
                    niBits='01'
                elif '@' in finalArr[i][2] : #law indirect
                    niBits='10'
                else : #law tabee3y
                    niBits='11'
                #keda ma3ana el op,ni,ne5osh 3al x

                if ',X' in finalArr[i][2]:
                    xBits = '1'
                else :
                    xBits='0'
                #nebda2 fel b wel p

                if '+' in finalArr[i][1] or '#' in finalArr[i][2]: #keda format4 el TA=disp
                    bpBits='00'
                else :#8er keda el default pc relative unless law tala3lena address out of range
                    bpBits='01'

                #nebda2 fel e

                if '+' in finalArr[i][1]: #keda format4 el e bit be 1
                    eBits='1'
                else :#keda format 3 yeb2a el e bit be 0
                    eBits='0'
                #neegy ba2a lel address bits

                if '+' in finalArr[i][1]:  # keda format4 el TA = directly el displacement
                    wholeAddressStr=ToolsFile.findAddress(finalArr[i][2]).zfill(5)
                else: #hena law 3ayez ageeb address fe format 3 nebtedy ba2a
                    if '#' in finalArr[i][2] :
                        if finalArr[i][2].replace('#','').isdigit():
                            immediate = finalArr[i][2].replace('#','')
                            wholeAddressStr=immediate.zfill(3)
                    else:
                        firstAddress=ToolsFile.findAddress(finalArr[i][2]) #keda law heya pc relative
                        secondAddress=ToolsFile.findpc(i)
                        wholeAddress=hex(int(firstAddress,16)-int(secondAddress,16)).split('x')[-1].upper()
                        if len(wholeAddress)> 3 : #keda law heya base relative
                            secondAddress=ToolsFile.findBase() #hat address el base
                            wholeAddress = hex(int(firstAddress,16)-int(secondAddress,16)).split('x')[-1].upper()# we etra7o men el location
                        #we hayb2a howa dah el address beta3na
                        wholeAddressStr = str(wholeAddress).zfill(3)
                part1objBin=(opBits+''+niBits+''+xBits+''+bpBits+''+eBits) #gma3 nos el obj code in binary
                part1objInt=(int(part1objBin,2)) #7awelo int
                part1objhex=hex(part1objInt).split('x')[-1].upper().zfill(3) #then hex
                objectcodeFile.write(part1objhex+''+wholeAddressStr+'\n') #then 7otto fel file gambo el address

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
    #to get the m record
    Modification = getMrecord()
    # To get the end (E.)
    End = str("E." + ToolsFile.startingadress().zfill(6))

    # We assigned our initiatives for the loop below
    Count = 0
    TStart = ToolsFile.startingadress()
    Tobj = ""  # A temp that carries T record

    # To get the text (T.)
    for i in range(len(ObjectCodeArray)):  # We loop through the Object Code file
        # The break condition of the Text record
        if ("No object code!" in ObjectCodeArray[i]):
            if Tobj != "":  # As long as Tobj doesn't equal to ""
                HTE_File.write(hex(Count).split(
                    'x')[-1].upper().zfill(2)+""+str(Tobj).replace("\n", "")+"\n")
            Count = 0
            Tobj = ""
        elif (Count >= 25):  # The other break condition of the Text record
            if Tobj != "":  # We put it due to a bug not properly executing the lines below
                HTE_File.write(hex(Count).split(
                    'x')[-1].upper().zfill(2)+""+str(Tobj).replace("\n", "")+"\n")
            Count = int((len(ObjectCodeArray[i]) - 1)/ 2)  # RELATED: we put the counter to 3 because we used a word in the T record
            HTE_File.write("T." + LArray[i].zfill(6).replace("\n", "") + ".")
            Tobj = ("."+ObjectCodeArray[i])

        elif i == len(ObjectCodeArray) - 1:  # When the text record reaches the end
            if Tobj != "":
                HTE_File.write(hex(Count).split(
                    'x')[-1].upper().zfill(2) + "" + str(Tobj).replace("\n", "") + "\n")
            for i in range(len(Modification)):
                HTE_File.write(Modification[i]+"\n")
            HTE_File.write(End)
        else:
            if Count == 0 and '-----' not in LArray[i]:  # RELATED: the reason why we made the count = 3 above was
                # we wouldn't be able to execute the others below and make a new T-record
                HTE_File.write(
                    "T." + LArray[i].zfill(6).replace("\n", "") + ".")
            elif Count == 0 and '-----' in LArray[i]:  # RELATED: the reason why we made the count = 3 above was
                # we wouldn't be able to execute the others below and make a new T-record
                HTE_File.write(
                    "T." + LArray[i+1].zfill(6).replace("\n", "") + ".")
            Count = Count+int((len(ObjectCodeArray[i]) - 1)/ 2)
            Tobj = (Tobj+"."+ObjectCodeArray[i])

    HTE_File.close()