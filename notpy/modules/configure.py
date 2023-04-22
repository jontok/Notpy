import os
import json
import shutil
from pathlib import Path

base_config = {
    "paths": {
        "homeDir": "",
        "notebookDir": "/Notpy"
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

default_config_file = str(Path.home()) + "/.config/notpy/config.json"

config = {}

def getConfigFile(config_file=default_config_file):
    if os.path.exists(config_file):        
        with open(config_file, "rb") as f:
            json_data = json.load(f)
            f.close()
            return json_data

def initConfigFile(path, config_file):
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(config_file):
        with open(config_file, "w") as f:
            json.dump(base_config, f)
            f.close()        
    with open(config_file, "rb") as f:
        json_data = json.load(f)
        f.close()
        return json_data

def setConfigFile(config_file, config):
    with open(config_file, "r+") as f:
        f.seek(0)
        json.dump(config, f)
        f.close()

def getDefaultPage():
    with open(str(Path.home()) + "/.local/lib/python3.10/site-packages/notpy/modules/README.md", "r") as readme:
        default_md = readme.read()
        return default_md

def generatePageObject(config, notebook_id, pg_dir):
    page_obj = {
        "id": len(config["notebooks"][notebook_id]["pages"]),
        "name": pg_dir
    }

    return page_obj


def setupNotpy(config_file, config):
    
    homeDir = str(input("home directory (default: /home/$USER)"))
    config["paths"]["homeDir"] = homeDir
    if homeDir == "":
        
        config["paths"]["homeDir"] = str(Path.home())
    

    notebookDir = str(input("How do you want to call the notebook directory (default: /Notpy) "))
    config["paths"]["notebookDir"] = notebookDir
    if notebookDir == "":
        config["paths"]["notebookDir"] = "/Notpy"

    notebookPath = str(config["paths"]["homeDir"]) + str(config["paths"]["notebookDir"])
    if not os.path.exists(notebookPath):
        os.mkdir(notebookPath)
    

    defaultBook = str(input("Do you want to create the default notebook (default: yes) y/n: "))
    match defaultBook:
        case "y" | "yes" | "":
            defaultNotebookDir = str(notebookPath) + "/" + str(config["notebooks"][0]["name"])
            if not os.path.exists(defaultNotebookDir):
                os.mkdir(defaultNotebookDir)
            defaultPagePath = defaultNotebookDir + "/" + config["notebooks"][0]["pages"][0]["name"]
            if not os.path.exists(defaultPagePath):
                with open(defaultPagePath, "x") as defaultPage:
                    defaultPage.write(getDefaultPage())
                    return "done"
        case "n" | "no":
            return "done"
        case _:
            print ("Not a valid value")

    config["setup"] = True
    shutil.copyfile(str(Path.home()) + "/.local/lib/python3.10/site-packages/notpy/modules/style.css", str(Path.home()) + "/.config/notpy/style.css")
    setConfigFile(config_file, config)
    print("Setup finished")

def editConfig():
    print("Configuration File located in $HOME/.config/notpy")
    home = str(Path.home())
    path = home + "/.config/notpy"
    config_file = path + "/config.json"
    config = initConfigFile(path,config_file)
    if config["setup"] != False:
        reconfigure = str(input("Want to reconfigure Notpy? (Y/n)"))
        match reconfigure:
            case "y" | "Y" | "yes":
                setupNotpy(config_file, config)
            case "n" | "no":
                print("Skipping")
            case _:
                print("Not a valid value")
    else:
        setupNotpy(config_file, config)