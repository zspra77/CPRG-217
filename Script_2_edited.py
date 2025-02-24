"""
Script_2.py

Reads system information from a JSON file and displays details about the machine name, system accounts, CPU information, and running services.

CPRG217-A, Feb 23, 2025
Group 8,
Muhammad Khan 957149,
...
"""

#Define the JSON file containing the system information
JSON_FILE_NAME = "Assignment_2.json"

import json

#validates and opens machine log file
def ReadJsonFile():
    try:
        with open(JSON_FILE_NAME) as rFile:
            dictionary = json.load(rFile)
    except:
        print("Could not load json file")

    return dictionary

#get and display machine name
def PrintMachineName():
    machineName = dictionary["machineName"]
    print("Machine name =", machineName)
    
#get and display groups and associated accounts
def PrintSystemAccounts():
    systemAccounts = dictionary["systemAccounts"]
    print("\t" +"System accounts and associated groups")
    for account in systemAccounts:
        print(account[0])
        for groupName in account[1]:
            print("\t", groupName)
            
#get and display cpu info
def PrintCpuInfo():
    cpuInfo = dictionary["cpuInfoData"]
    for line in cpuInfo:
        print(line)

#get and display services
def PrintAllServices():
    allServices = dictionary["allServices"]
    for service in allServices:
        print(service)

#Main
dictionary = ReadJsonFile() 
print()
PrintMachineName()
print()
PrintSystemAccounts()
#display title for cpu info with proper formating
print("\n" + "\t" + "CPU Info")
PrintCpuInfo()
#display title for services with proper formating
print("\n" + "\t" + "All Running Services")
PrintAllServices()
