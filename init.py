import os, json, time, backups
from shared_functions import *
global Files
Files = {}
Files["RAMOnly"] = False
defaultConfig = {
    "autoBackup" : False,
    "backupFolderPath" : str(os.getcwd()) + "\\backups",
    "hoursOfBackup" : [],
    "pathsToBackup" : []
}


def initFiles():
    global Files
    Files["Config"] = initConfig()
    Files["Config"]["hoursOfBackup"] = validateBackupHours(Files["Config"]["hoursOfBackup"])
    Files["Config"]["pathsToBackup"] = validateBackupPaths(Files["Config"]["pathsToBackup"])
    backups.startBackups()

def initBackupsFolder(backupPath):
    if not os.path.exists(backupPath):
        notify("warning","Backup's directory doesn't exist. Creating new backup's folder.", True)
        try:
            os.mkdir(backupPath)
        except Exception as e:
            notify("error","Cant create backup's folder.", True)
        else:
            notify("info","Sucessfully created backup's folder.", True)

def initConfig():
    try:
        configFile = open("config.json", "r")
    except:
        notify("error","Error occured with 'config.json' file, creating new one.", True)
        Config = createDefaultConfig()
    else: 
        Config = validateConfig(configFile.read())
        return Config
        
def validateConfig(cfgFile):
    try:
        cfgFile = json.loads(cfgFile)
        if not "backupFolderPath" in cfgFile:
            initBackupsFolder(defaultConfig["backupFolderPath"])
        else:
            initBackupsFolder(cfgFile["backupFolderPath"])
    except:
        notify("error","Something went wrong with 'config.json' file, creating new one.", True)
        cfgFile = createDefaultConfig()
        initBackupsFolder(defaultConfig["backupFolderPath"])
    else:
        for k in defaultConfig:
            if k not in cfgFile:
                notify("warning","Key '"+k+"' missing in 'config.json'. Adding default value.", True)
                cfgFile[k] = defaultConfig[k]
                saveFile("config.json", cfgFile)
            else:
                if cfgFile[k] == None:
                    cfgFile[k] = defaultConfig[k]
                    notify("warning","Key '"+k+"' is None in 'config.json'. Adding default value.", True)
                    saveFile("config.json", cfgFile)
        return cfgFile

def createDefaultConfig():
    notify("info","Creating new Config file", True)
    try:
        newConfigFile = open("config.json", "w")
    except:
        notify("error","Problem while creating 'config.json' file, using default config dictionary.", True)
        notify("warning",'all created changes WILL NOT be saved. Working in RAM-only mode.', True)
        Files["RAMOnly"] = True
        initBackupsFolder(defaultConfig["backupFolderPath"])
        return defaultConfig
    else:
        json.dump(defaultConfig, newConfigFile)
        notify("info","Sucessfully created new 'config.json' file.", True)
        initBackupsFolder(defaultConfig["backupFolderPath"])
        return defaultConfig

def saveFile(file, content):
    notify("info","Saving "+file)
    try:
        newFile = open(file, "w")
    except:
        notify("error","Problem while saving '"+file+"'.", True)
    else:
        json.dump(content, newFile)
        notify("info", "Sucessfully saved '"+file+"'.", True)

