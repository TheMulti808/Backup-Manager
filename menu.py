import os
from menu_functions import *
from shared_functions import *
from main import notify

menus = {}
menus["current"] = "start_menu"
menus["previous"] = "start_menu"
menus["start_menu"] = {
    "label" : "Backup Manager",
    "description": "Welcome in Backup Manager. Let's start!",
    "options" : {
        "1" : "Check current status",
        "2" : "Create backup",
        "3" : "Edit config",
        "0" : "Exit program",
    }
}

menus["backup_menu"] = {
    "label" : "Backup Menu",
    "description": "Manage your backup's",
    "options" : {
        "1" : "Backup all stored path's",
        "2" : "Backup new path",
        "0" : "Go back",

    }
}

menus["edit_config"] = {
    "label" : "Edit Menu",
    "description": "Edit your config.",
    "options" : {
        "1" : "Change autobackup status",
        "2" : "Change backup folder path",
        "3" : "Change backup hours",
        "4" : "Change paths to backup",
        "0" : "Go back",
    }
}

menus["autobackup_menu"] = {
    "label" : "Autobackup Menu",
    "description": "Change autobackup option",
    "options" : {
        "1" : "Autobackup ON",
        "2" : "Autobackup OFF",
        "0" : "Go back",

    }
}


def initiateMenu():
    while True:
        os.system('cls')
        print( 30 * "-" , menus[menus["current"]]["label"] , 30 * "-")
        print(menus[menus["current"]]["description"], "\n")
        for k in menus[menus["current"]]["options"]:
            print("( "+k+" ) - "+menus[menus["current"]]["options"][k])
        choice = input("\nChoose your option: ")
        if not choice in menuFunctions[menus["current"]]:
            notify("error", "Choosen option is not valid. Press enter to continue...", True)
            input("")
            os.system('cls')
        else:
            menuFunctions[menus["current"]][choice]()
