"""
Script_1.py

Aquires system information such as machine name, CPU details, running services, and system accounts, then stores the data in a JSON file.

CPRG217-A Feb 10/25
Group 8 
Muhammad Khan 957149, Xiangzhi Gu 538190
"""

import socket, pwd, grp, os, json

#Define the file path for CPU information
CPU_INFO_FILE = "/proc/cpuinfo"

#get the host name of the machine
def GetMachineName():
    machineName = socket.gethostname()
    return machineName

#open the cpu info file and append every line of information into an array
def GetCpuInfo():
    '''
    uses system cpu file location to get cpu information.
    '''
    try:
        rFile = open(CPU_INFO_FILE, "r")
        dataArray = rFile.read().splitlines()
        rFile.close()
    except:
        print("CPU info file could not be read!")
    
    cpuInfoData = []
    criteriaArray = ["processor", "vendor_id", "model", "model name", "cache size"]

    #Extracts the first occurrence of each relevant CPU info field
    for criteria in criteriaArray:
        for line in dataArray:
            if criteria in line:
                cpuInfoData.append(line)
                break

    return cpuInfoData
            
#get every line of services log
def GetAllServices():
    allServices = os.popen("systemctl list-units --type=service").read().splitlines()

    return allServices

#get users name and group membership information
def SystemAccountInfo():
    '''
    check the membership of the user by accessing the groupid of user and referencing group record.
    Uses case sensitive sorting
    '''
    systemAccounts = []
    allRecords = pwd.getpwall()
    for record in allRecords:
        accountName = record.pw_name
        defaultGroupId = record.pw_gid
        defaultGroupRecord = grp.getgrgid(defaultGroupId)
        groupMembership = [defaultGroupRecord.gr_name]
        allGroups = grp.getgrall()
        for groupRecord in allGroups:
            groupMem = groupRecord.gr_mem
            if accountName in groupMem:
                groupName = groupRecord.gr_name
                groupMembership.append(groupName)
        systemAccounts.append([accountName, groupMembership])

    #Sort all accounts based on the account name
    sortedTable = sorted(systemAccounts, key = lambda record:record[0].lower())



    return systemAccounts

#log file of machine, accounts, cpu infor, and active services on machine
def WriteJsonFile():
    '''
    create a log file call Assignment_2.json of relevant machine log information
    '''
    myDictionary = {"machineName": machineName, "systemAccounts": systemAccounts, "cpuInfoData": cpuInfoData, "allServices": allServices}

    try:
        with open("Assignment_2.json", "w") as rFile:
            json.dump(myDictionary, rFile, indent=2)
        print("Wrote Json file!")

    except:
        print("Could not write Json file")
    

#Main
machineName = GetMachineName()
systemAccounts = SystemAccountInfo()
cpuInfoData = GetCpuInfo()
allServices = GetAllServices()

#Write data to json file
WriteJsonFile()






"""
for account in systemAccounts:
    print(account[0])
    for groupName in account[1]:
        print("\t", groupName)
"""


