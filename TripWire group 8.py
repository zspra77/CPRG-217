"""
TripWire.py

Checks the integrity of a folder structure/files for any changes using a hashvalue

How to run at commandline:
To create record use the following pattern:
    "python3 TripWire.py TripWireDirectory TripWire_Record.txt c
To test against the record use the following pattern:
    "python3 TripWire.py TripWire_Record.txt"

CPRG-217-A  Feb. 2, 2025
group 8
Clayton Ma 760796, Allen Amil 959926, Muhammad Khan 957149


"""

#utilize 'import' to allow the script to access files within a user's operating system to check data files. A
import hashlib, sys, os

#separate the filename and hash value for a more readable view. A
DELIMITER = ":"





#testFolder = "/home/student/Documents/CPRG217/Spring_2024/Section_A/Assignment_1/testFolder"
#recordFile = "TripWire_Record.txt"





#uses the ls command to list files in test folder and seperates them into individual lines
def GetFileList():
    fileList = os.popen("ls " + testFolder).read().splitlines() 
    return fileList



def GetHash(fileName):
    #format the given arguments in a readable path for the code to access exact file. A
    filePath = testFolder + "/" + fileName
    try:
        refFile = open(filePath, "rb") #opens the file and reads it in binary to get the data
        data = refFile.read()
        refFile.close()
    except:
        print("The following file could not be read:", filePath)

    hashResult = hashlib.md5(data).hexdigest()  #returns the hash result on the data and converts to hexidecimal
    return hashResult



#opens the record file and writes the filename and hash value with delimiter :
def WriteRecord():
    try:
        refFile = open(recordFile, "w")
        refFile.write(testFolder + "\n")
        for fileName in fileList:
            hashResult = GetHash(fileName)
            refFile.write(fileName + DELIMITER + hashResult + "\n")
        refFile.close()
    except:
        print("Could not write to record file!")
    print("Record was created!")



#creates an empty list to store the filename and hash value pairs
def ReadRecordFile():
    try:
        refFile = open(recordFile, "r")
        lines = refFile.read().splitlines()
        refFile.close()
    except:
        print("Could not read record file!")

    recordTable = []
    firstLine = True
    for line in lines:
        if firstLine == True:     #this is used to skip the first line which is the folder path
            firstLine = False
        else:
            splitLine = line.split(DELIMITER)
            recordTable.append(splitLine)
    return recordTable



#keeps a record of previously recorded filenames
def GetOldFileList(recordTable):
    oldFileList = []
    for row in recordTable:
        oldFileList.append(row[0])
    return oldFileList
    


#compares the previously stored filenames to the currently stored filenames and seperates them into categories
def SortBuckets():
    missingFiles = []
    possiblyModified = []
    currentFileList = GetFileList()
    recordTable = ReadRecordFile()
    oldFileList = GetOldFileList(recordTable)
    for fileName in oldFileList:
        if fileName in currentFileList:
            possiblyModified.append(fileName)
            currentFileList.remove(fileName)
        else:
            missingFiles.append(fileName)
    additionalFiles = currentFileList

    return missingFiles, additionalFiles, possiblyModified, recordTable



# checks that filenames have matching hash value as previously recorded versions
def CheckIfModified():
    modifiedFiles = []
    for fileName in possiblyModified:
        for row in recordTable:
            if row[0] == fileName:
                if row[1] != GetHash(fileName):
                    modifiedFiles.append(fileName)
    return modifiedFiles



def GetFolderPath():
    testFolder = ""
    try:
        refFile = open(recordFile, "r")
        data = refFile.read().splitlines()
        refFile.close()
        testFolder = data[0]
    except:
        print("Could not read the file", recordFile)
    return testFolder
        
    



#MAIN 
#Get current working directory path
#reads commandline arguments
argList = sys.argv





#verifies that user has entered valid folder path, if not instructions are printed
if len(argList) < 2:
    print("To create record use the following pattern:")
    print("\t" + "python3 TripWire.py TripWireDirectory TripWire_Record.txt c")
    print("To test against the record use the following pattern:")
    print("\t" + "python3 TripWire.py TripWire_Record.txt")
else:
    if len(argList) > 2:
        #PART 1
        testFolder = argList[1]
        recordFile = argList[2]
        fileList = GetFileList()
        WriteRecord()

    else:
        #PART 2
        recordFile = argList[1]
        recordFileExists = os.path.exists(recordFile)
        if recordFileExists:
            testFolder = GetFolderPath()
            if testFolder != "":
                #Sort files
                missingFiles, additionalFiles, possiblyModified, recordTable = SortBuckets()
                modifiedFiles = CheckIfModified()

                #check for new, missing and modified files
                print("missingFiles: ")
                for fileName in missingFiles:
                    print("\t" + fileName)
                print("additionalFiles: ")
                for fileName in additionalFiles:
                    print("\t" + fileName)
                print("modifiedFiles: ")
                for fileName in modifiedFiles:
                    print("\t" + fileName)

        else:
            print("No record by that name exists!")
            
#END OF SCRIPT
