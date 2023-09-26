import os, sys, main, menu, time, init, re, backups
from datetime import datetime
from shared_functions import *

menuFunctions = {}


def checkCurrentStatus():
    currentVariables = main.getSystemVariables()
    os.system('cls')
    backupedFiles = len([entry for entry in os.listdir(init.Files["Config"]["backupFolderPath"]) if os.path.isfile(os.path.join(init.Files["Config"]["backupFolderPath"], entry))])
    print( 30 * "-" , 'Backup status' , 30 * "-","\n")
    print("( Current Status ) ", "Already backuped "+str(backupedFiles)+" files!")
    print("( Program start time ) ", currentVariables["start_time"])
    print("( Current time ) ", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    input("\nPress enter to continue...")

def autoBackupOn():
    init.Files["Config"]["autoBackup"] = True
    init.saveFile("config.json", init.Files["Config"])
    os.system('cls')
    notify("info", "Autobackup changed to: Enabled")
    time.sleep(1)
    openEditConfigMenu()

def autoBackupOff():
    init.Files["Config"]["autoBackup"] = False
    init.saveFile("config.json", init.Files["Config"])
    os.system('cls')
    notify("info", "Autobackup changed to: Disabled")
    time.sleep(1)
    openEditConfigMenu()

def backupAllStoredPaths():
    os.system('cls')
    notify("info","Creating backups of all stored paths!", True)
    time.sleep(2)
    backups.backupAllStoredPaths()
    return

def backupNewPath():
    os.system('cls')
    print( 30 * "-" , 'Backup new path' , 30 * "-","\nEnter path to backup or '0' to cancel!\n")
    path = input("Enter path to backup: ")
    if str(path) == "0": return
    if not os.path.exists(path):
        print("This path does not exists! Try again")
        time.sleep(1)
        backupNewPath()
        return
    backups.createBackupPathThread(path)
    return


def changeBackupFolder():
    errorMessage = None
    while True:
        os.system('cls')
        path = init.Files["Config"]["backupFolderPath"]
        if path == 'backups':
            path = str(os.getcwd()) + "\\backups"
        print( 30 * "-" , 'Change Backup Folder' , 30 * "-","\n")
        print("( Current Path ) - ", path)
        print("Press only enter to cancel")
        print(errorMessage != None and errorMessage or "")
        newPath = input("Enter new path: ")
        if newPath == "": 
            break 
            openEditConfigMenu()
        if not os.path.exists(newPath):
            errorMessage = "This path doesn't exist's. Please try again or leave empty input to go back."
        else:
            confirm = input("New path is: "+newPath+". \nConfirm by entering 'confirm': ")
            if confirm == "confirm":
                os.system('cls')
                init.Files["Config"]["backupFolderPath"] = newPath
                init.saveFile("config.json", init.Files["Config"])
                notify("info", "Backup folder path changed to: "+newPath, True)
                time.sleep(2)
                break
                openEditConfigMenu()

def changeBackupHours():
    addNewHours = False
    os.system('cls')
    print( 30 * "-" , 'Change Backup hours' , 30 * "-","\n")
    currentHours = init.Files["Config"]["hoursOfBackup"]
    if len(currentHours) == 0:
        while True:
            print("Backup hours are not set yet. Do you want to set new hours?")
            print("( 1 ) - Yes")
            print("( 2 ) - No")
            decision = str(input("Choose your option: "))
            if decision == "1":
                addNewHours = True
            else:
                return
            if addNewHours:
                break
        if addNewHours:
            createNewBackupHours(currentHours)
    else:
        createNewBackupHours(currentHours)



def createNewBackupHours(currentHours):
    currentHours = sorted(currentHours)
    currentHours = validateBackupHours(currentHours)
    regex = re.compile("^(?:[01]?\d|2[0-3])(?::[0-5]\d){1,2}$")
    while True:
        os.system('cls')
        print( 30 * "-" , 'Change Backup hours' , 30 * "-","\n")
        print("Current backup hours:")
        tempHoursVar = {}
        tempIteration = 1
        for hour in currentHours:
            tempHoursVar[str(tempIteration)] = hour
            print("( "+str(tempIteration)+" ) - "+hour)
            tempIteration += 1
        print("\n[INSTRUCION]: Enter ID of hour to DELETE it")
        print("[INSTRUCION]: Enter new hour in format: '00:00' to add it")
        print("[INSTRUCION]: Enter '0' to finish and return to previous menu\n")
        action = input("Your action: ")
        if str(action) == "0":
            currentHours = []
            for hours in tempHoursVar:
                currentHours.append(tempHoursVar[hours])
            init.Files["Config"]["hoursOfBackup"] = currentHours
            init.saveFile("config.json", init.Files["Config"])
            backups.createBackupsSchedule()
            openEditConfigMenu()
            break
        elif str(action) in tempHoursVar:
            currentHours.remove(tempHoursVar[str(action)])
        else:
            if ":" in action:
                result = re.search(regex, action)
                if result is None :
                    print("Wrong time format! Try to use HOURS:MINUTES!")
                    time.sleep(2)
                    continue
                else:
                    currentHours.append(action)
                    continue
            else:
                print("Wrong time format! Try to use HOURS:MINUTES!")
                time.sleep(2)
                continue


def changePathsToBackup():
    addNewPaths = False
    os.system('cls')
    print( 30 * "-" , 'Change Backup paths' , 30 * "-","\n")
    currentPaths = init.Files["Config"]["pathsToBackup"]
    if len(currentPaths) == 0:
        while True:
            print("Backup paths are not set yet. Do you want to add new paths?")
            print("( 1 ) - Yes")
            print("( 2 ) - No")
            decision = str(input("Choose your option: "))
            if decision == "1":
                addNewPaths = True
            else:
                return
            if addNewPaths:
                break
        if addNewPaths:
            createNewBackupPaths(currentPaths)
    else:
        createNewBackupPaths(currentPaths)

def createNewBackupPaths(currentPaths):
    currentPaths = sorted(currentPaths)
    errorMessage = None
    while True:
        os.system('cls')
        print( 30 * "-" , 'Change Backup paths' , 30 * "-",errorMessage != None and "\nERROR: "+errorMessage or "\n")
        errorMessage = None
        print("Current backup paths:")
        tempPathsVar = {}
        tempIteration = 1
        for path in currentPaths:
            tempPathsVar[str(tempIteration)] = path
            print("( "+str(tempIteration)+" ) - "+path)
            tempIteration += 1
        print("\n[INSTRUCION]: Enter ID of path to DELETE it")
        print("[INSTRUCION]: Enter new path to add it")
        print("[INSTRUCION]: Enter '0' to finish and return to previous menu\n")
        action = input("Your action: ")
        if str(action) == "0":
            currentPaths = []
            for hours in tempPathsVar:
                currentPaths.append(tempPathsVar[hours])
            init.Files["Config"]["pathsToBackup"] = currentPaths
            init.saveFile("config.json", init.Files["Config"])
            backups.createBackupsSchedule()
            openEditConfigMenu()
            backups.createBackupsSchedule()
            break
        elif str(action) in tempPathsVar:
            currentPaths.remove(tempPathsVar[str(action)])
            notify("info", "Path "+str(action)+" sucessfully removed from backups", True)

        else:
            if not os.path.exists(action):
                errorMessage = "Wrong path entered!"
                continue
            else:
                if action in currentPaths:
                    notify("error", "Path already exists in config.", True)
                    time.sleep(2)
                    continue
                currentPaths.append(action)
                notify("info", "Path "+action+" sucessfully added to backups", True)

def closeProgram():
    notify("info", "Closing program", True)
    os.system('cls')
    print("Thank you for using Backup Manager!")
    sys.exit()



def openCreateBackupMenu():
    menu.menus["current"] = "backup_menu"
    menu.menus["previous"] = "start_menu"

def openEditConfigMenu():
    menu.menus["current"] = "edit_config"
    menu.menus["previous"] = "start_menu"

def changeAutobackupMenu():
    menu.menus["current"] = "autobackup_menu"
    menu.menus["previous"] = "backup_menu"

def goBackToPreviousMenu():
    if menu.menus["current"] == menu.menus["previous"]:
        menu.menus["current"] = "start_menu"
        menu.menus["previous"] = "start_menu"
        os.system('cls')
        return
    menu.menus["current"] = menu.menus["previous"] 
    os.system('cls')






menuFunctions["start_menu"] = {
    "1": checkCurrentStatus,
    "2": openCreateBackupMenu,
    "3": openEditConfigMenu,
    "0": closeProgram
}
menuFunctions["backup_menu"] = {
    "1": backupAllStoredPaths,
    "2": backupNewPath,
    "0": goBackToPreviousMenu
}
menuFunctions["edit_config"] = {
    "1": changeAutobackupMenu,
    "2": changeBackupFolder,
    "3": changeBackupHours,
    "4": changePathsToBackup,
    "0": goBackToPreviousMenu
}
menuFunctions["autobackup_menu"] = {
    "1": autoBackupOn,
    "2": autoBackupOff,
    "0": goBackToPreviousMenu
}