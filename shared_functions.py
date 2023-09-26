import logging, os, init, re, time
from datetime import datetime
logger = None

def notify(*args):
    channel = args[0]
    message = args[1]
    doPrint = args[2]
    if not channel or not message: return
    if channel == 'info':
        if doPrint: print("INFO: "+message)
        if logger: logger.info(message)
    elif channel == 'error':
        if doPrint: print("ERROR: "+message)
        if logger: logger.error(message)
    elif channel == 'warning':
        if doPrint: print("WARNING: "+message)
        if logger: logger.warning(message)
    else:
        if logger: logger.debug(message)
    #This is handler for you to use with discord webhook, email notification, or anything else.

if not os.path.exists("logs"):
    notify("warning","Logs's directory doesn't exist. Creating new log's folder.", True)
    try:
        os.mkdir("logs")
    except Exception as e:
        notify("error","Cant create log's folder.", True)
    else:
        notify("info","Sucessfully created log's folder.", True)

currentDate = str(datetime.now().strftime("%d.%m.%Y %H-%M-%S"))
logging.basicConfig(filename="logs/"+currentDate+".log",
    format='%(asctime)s %(message)s',
    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def validateBackupHours(hours):
    regex = re.compile("^(?:[01]?\d|2[0-3])(?::[0-5]\d){1,2}$")
    anyChanges = False
    for hour in hours:
        result = re.search(regex, hour)
        if result is None :
            anyChanges = True
            notify("warning","Removing '"+hour+"' from hours due to wrong format.", True)
            hours.remove(hour)
    if anyChanges:
        init.Files["Config"]["hoursOfBackup"] = hours
        init.saveFile("config.json", init.Files["Config"])
    return hours

def validateBackupPaths(paths):
    anyChanges = False
    for path in paths:
        if not os.path.exists(path):
            anyChanges = True
            notify("warning","Removing \n'"+path+"'\n from backup paths. Probably wrong format or directory doesn't exist.", True)
            paths.remove(path)
            time.sleep(0.5)
    if anyChanges:
        init.Files["Config"]["pathsToBackup"] = paths
        init.saveFile("config.json", init.Files["Config"])
    return paths