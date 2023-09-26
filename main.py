import os, init, time, menu, sys
from shared_functions import *
from datetime import datetime
SystemVariables = {
    "Files" : {},
    "start_time": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
}

tryCount = 0
def getSystemVariables():
    return SystemVariables

def updateSystemVariable(variableName, variableValue):
    SystemVariables[variableName] = variableValue


def main():
    global tryCount
    try:
        init.initFiles()
    except Exception as e:
        if tryCount > 5:
            notify("error","Cant start the program. Contact with author.", True)
            sys.exit()
        notify("error","Something went wrong! Trying again.", True)
        tryCount += 1
        time.sleep(0.5)
        main()
    else:
        notify("info","Everything is ready! Starting menu!", True)
        os.system('cls')
        menu.initiateMenu()


if __name__ == '__main__': main()