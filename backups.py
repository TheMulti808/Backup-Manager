import time,  init, shutil, threading, schedule
from shared_functions import *

backupThreads = {}

def startBackups():
    backupThreads["schedule"] = threading.Thread(name="schedule", target=createScheduleThread)
    backupThreads["schedule"].start()
    createBackupsSchedule()


def createScheduleThread():
    notify("info", "Scheduling thread created.", False)
    while True:
        if init.Files["Config"]["autoBackup"]:
            schedule.run_pending()
        time.sleep(1)

def createBackupsSchedule():
    schedule.clear('scheduled-backup')
    if len(init.Files["Config"]["hoursOfBackup"]) == 0:
        notify("error", "There is no scheduled hours to backup!", True)
        return    
    if len(init.Files["Config"]["pathsToBackup"]) == 0:
        notify("error", "There is no paths to backup!", True)
        return
    for hour in init.Files["Config"]["hoursOfBackup"]:
        for path in init.Files["Config"]["pathsToBackup"]:
            schedule.every().day.at(hour).do(createBackupPathThread, path).tag("scheduled-backup")

def createBackupPathThread(*args):
    backupThreads[args[0]] = threading.Thread(name=args[0], target=backupPath, args=(args[0],))
    backupThreads[args[0]].start()

def backupAllStoredPaths():
    for path in init.Files["Config"]["pathsToBackup"]:
        createBackupPathThread(path)

def backupPath(*args):
    path = args[0]
    folderName = os.path.split(os.path.dirname(path+"\\"))[-1]
    folderName = folderName+"_backup "+str(datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
    backupedFilePath = init.Files["Config"]["backupFolderPath"]+"\\"+folderName
    notify("info","Started backup of "+path, False)
    archived = shutil.make_archive(backupedFilePath, 'zip', path)

    if os.path.exists(backupedFilePath+".zip"):
        notify("info","Backup of "+folderName+" created!", False)
    else: 
        notify("error","Cant create backup of "+folderName, False)
    del backupThreads[path]
    notify("info","Ended backup of "+path, False)