import os
import json
from pathlib import Path

base_config = {
    "paths": {
        "homeDir": "",
        "notebookDir": "/Notpy"
        "configDir" "" 
    },
    "notebooks": [
        {
            "id": 0,
            "name": "default",
            "pages": [
                {
                    "id": 0,
                    "name": "default.md"
                }
            ]
        }
    ],
    "setup": False

}

config = {}

def getConfigFile(path, config_file):
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(config_file):
        with open(config_file, "w") as f:
            json.dump(base_config, f)
            f.close()        
    with open(config_file, "rb") as f:
        config = json.load(f)
        f.close()
        #return config

def setConfigFile(config_file, config):
    with open(config_file, "r+") as f:
        print(config)

        json.dump(config, f)
        f.close()

def setupNotpy(config_file, config):
    
    homeDir = str(input("home directory (default: /home/$USER)"))
    config["paths"]["homeDir"] = homeDir
    if homeDir == "":
        config["paths"]["homeDir"] = Path.home()
    
    print(config["paths"]["homeDir"])

    notebookDir = str(input("How do you want to call the notebook directory (default: /Notpy) "))
    config["paths"]["notebookDir"] = notebookDir
    if notebookDir == "":
        config["paths"]["notebookDir"] = "/Notpy"

    notebookPath = str(config["paths"]["homeDir"]) + str(config["paths"]["notebookDir"])
    if not os.path.exists(notebookPath):
        os.mkdir(notebookPath)
    print(config["paths"]["notebookDir"])

    defaultBook = str(input("Do you want to create the default notebook (default: yes) y/n"))
    match defaultBook:
        case "y" | "yes":
            defaultNotebookDir = str(notebookPath) + "/" + str(config["notebooks"][0]["name"])
            if not os.path.exists(defaultNotebookDir):
                os.mkdir(defaultNotebookDir)
            defaultPagePath = defaultNotebookDir + "/" + config["notebooks"][0]["pages"][0]["name"]
            if not os.path.exists(defaultPagePath):
                with open(defaultPagePath, "x") as defaultPage:
                    return "done"
        case "n" | "no":
            return "done"

    config["setup"] = True
    setConfigFile(config_file, config)
    print("Setup finished")

def editConfig():
    print("Configuration File located in $HOME/.config/notpy")
    home = str(Path.home())
    path = home + "/.config/notpy"
    config_file = path + "/config.json"
    config = getConfigFile(path,config_file)
    if config["setup"] != False:
        print(config["setup"])
    else:
        print(config["paths"]["homeDir"])
        setupNotpy(config_file, config)


    

