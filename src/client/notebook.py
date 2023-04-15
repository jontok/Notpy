import os
import json
from client.configure import getConfigFile, setConfigFile
from pathlib import Path

config_file = str(Path.home()) + "/.config/notpy/config.json"

def scanNotebooks():
    print("Scanning for pages and notebooks")

def createNotebook(config):
    notebookDir = str(config["paths"]["homeDir"]) + str(config["paths"]["notebookDir"])
    name = str(input("Notebook Name: "))
    print(name)
    new_notebook_path = notebookDir + "/" + name
    if not os.path.exists(new_notebook_path):  
        new_notebook = {
            'id': len(config["notebooks"]),
            'name': name,
            'pages': []
        }
        config["notebooks"].append(new_notebook)
        setConfigFile(config_file,config)
        os.mkdir(new_notebook_path)
    else:
        print("Notebook " + name + "already exists")

def createPage(config):
    print("Page created")

def deletePage(config):
    print("Page deleted")

def deleteNotebook(config):
    print("Delete notebook")
    notebookDir = str(config["paths"]["homeDir"]) + str(config["paths"]["notebookDir"])
    listNotebook(config)
    notebook = input("Notebook Id: ")
    if notebook != "":
        notebook_int = int(notebook)
        del_notebook = config["notebooks"][notebook_int]["name"]
        del_path = notebookDir + "/" + del_notebook
        if os.path.exists(del_path):
            confirm_delete = str(input("Delete " + del_notebook + " (Y/n) : "))
            match confirm_delete:
                case "y" | "Y":
                    for idx, obj in enumerate(config['notebooks']):
                        if obj["id"] == notebook_int:
                            print(notebook)
                            print(idx)
                            config["notebooks"].remove(obj)
                            print(config)
                        
                        with open(config_file, "w") as f:
                            f.seek(0)
                            json.dump(config, f)
                            f.close()

                    os.rmdir(del_path)
                case _:
                    print(del_notebook + " was not deleted")
        else:
            print("Folder does not exist")
    else:
        print("Not a valid input")
    
def listNotebook(config):
    print("id" + " | " + "name")
    print("--------")
    for nb in config["notebooks"]:
        print(str(nb["id"]) + "  | " + nb["name"])

def listPages(config, notebook_id):
    listNotebook(config)
    if notebook_id != "":
        print("id" + " | " + "name")
        print("--------")
        for nb in config["notebooks"][int(notebook_id)]["pages"]:
            print(str(nb["id"]) + "  | " + nb["name"])
    else:
        print("Not a valid input")

def getNotebookPage(config, notebook_id):
    page = input("PAge Id: ")
    notebook = config["notebooks"][int(notebook_id)]
    page_path = "/" + notebook["name"] + "/" + notebook["pages"][int(page)]["name"]
    print(page_path)
    return str(page_path)
     


def notebooks(config_file):
    config = getConfigFile(config_file)
    print("\nNotebook options:")
    print("1    - create notebook")
    print("2    - create page")
    print("3    - delete page")
    print("4    - delete notebook")
    print("5    - list notebooks")
    print("6    - list pages")
    task_str = input("Select an option: ")
    task = int(task_str)
    match task:
        case 1:
            createNotebook(config)
        case 2:
            createPage(config)
        case 3:
            deletePage(config)
        case 4:
            deleteNotebook(config)
        case 5:
            listNotebook(config)
        case 6:
            listNotebook(config)
            notebook_id = input("Notebook ID: ")
            listPages(config, notebook_id)
        case _:
            print("Not a valid value")
            
# while True:
#     notebooks(config_file)