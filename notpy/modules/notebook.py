import os
import json
from modules.configure import getConfigFile, setConfigFile
from pathlib import Path

config_file = str(Path.home()) + "/.config/notpy/config.json"


def scanNotebooks():
    print("Scanning for pages and notebooks")


def createNotebook(config,name):
    notebookDir = str(config["paths"]["homeDir"]) + str(config["paths"]["notebookDir"])
    new_notebook_path = notebookDir + "/" + name
    if not os.path.exists(new_notebook_path):
        new_notebook = {
            'id': len(config["notebooks"]),
            'name': name,
            'pages': []
        }
        config["notebooks"].append(new_notebook)
        setConfigFile(config_file, config)
        os.mkdir(new_notebook_path)
    else:
        print("Notebook " + name + " already exists")


def createPage(config):

    listNotebook(config)
    notebook_id = getUserInput("Select a notebook id: ", "int")
    listPages(config, notebook_id)
    page_name = getUserInput("Name your page: ", "str")
    if page_name[-3:] != ".md":
        page_name = page_name + ".md"
    config["notebooks"][notebook_id]["pages"].append(
        {
            "id": len(config["notebooks"][notebook_id]["pages"]),
            "name": page_name
        }
    )
    setConfigFile(config_file, config)
    file_path = getNotebookPagePath(config, notebook_id, page_name)
    Path(file_path).touch()

    print("Page created")


def deleteObjectFromConfig(config, del_object, id):
    for idx, obj in enumerate(del_object):
        if obj["id"] == id:
            del_object.remove(obj)
        with open(config_file, "w") as f:
            f.seek(0)
            json.dump(config, f)
            f.close()


def deletePage(config):
    notebookDir = getNotebookDirectory(config)
    listNotebook(config)
    notebook_id = getUserInput("Select a notebook id: ", "int")
    listPages(config, notebook_id)
    page_id = getUserInput("Select a page id: ", "int")
    relativ_path = getNotebookPage(config, notebook_id, page_id)
    del_path = notebookDir + relativ_path
    pages_obj = config['notebooks'][notebook_id]["pages"]
    confirm_delete = getUserInput("Do you want to delete " + del_path + " (Y/n): ")
    if os.path.exists(del_path):
        match confirm_delete:
            case "y" | "Y":
                deleteObjectFromConfig(config, pages_obj, page_id)
                os.remove(del_path)
                print("Page deleted")
            case _:
                print("Page not deleted")
    else:
        print("Page does not exist")
    


def deleteNotebook(config):
    print("Delete notebook")
    notebookDir = getNotebookDirectory(config)
    listNotebook(config)
    notebook_id = getUserInput("Notebook Id: ", "int")
    del_notebook = config["notebooks"][notebook_id]["name"]
    del_path = notebookDir + "/" + del_notebook
    if os.path.exists(del_path):
        confirm_delete = str(input("Delete " + del_notebook + " (Y/n) : "))
        match confirm_delete:
            case "y" | "Y":
                deleteObjectFromConfig(
                    config, config['notebooks'], notebook_id)

                os.rmdir(del_path)
            case _:
                print("The Notebook " + del_notebook + " was not deleted")
    else:
        print("Folder does not exist")


def getUserInput(prompt, return_type="str"):
    user_input = input(prompt)
    if user_input != "":
        match return_type:
            case "str":
                return str(user_input)
            case "int":
                return int(user_input)
    else:
        print("Not a valid input")


def listNotebook(config):
    print("id" + " | " + "name")
    print("--------")
    for nb in config["notebooks"]:
        print("" + str(nb["id"]) + "  | " + nb["name"])


def listPages(config, notebook_id):
    if notebook_id != "":
        print("id" + " | " + "name")
        print("--------")
        for nb in config["notebooks"][int(notebook_id)]["pages"]:
            print("" + str(nb["id"]) + "  | " + nb["name"])
    else:
        print("Not a valid input")


def getNotebookPage(config, notebook_id, page_id):
    notebook = config["notebooks"][int(notebook_id)]
    page_path = "/" + notebook["name"] + "/" + notebook["pages"][page_id]["name"]
    return str(page_path.replace(" ", "_"))


def getNotebookPagePath(config, notebook_id, page_name):
    if page_name[-3:] != ".md":
        page_name = page_name + ".md"
    home_dir = config["paths"]["homeDir"]
    nb_home_dir = config["paths"]["notebookDir"]
    nb_dir = config["notebooks"][notebook_id]["name"].replace(" ", "_")

    full_page_path = home_dir + nb_home_dir + "/" + nb_dir + "/" + page_name
    return str(full_page_path)


def getNotebookDirectory(config):
    notebookDir = str(config["paths"]["homeDir"]) + \
        str(config["paths"]["notebookDir"])
    return notebookDir

def getNotebookFromName(config,notebook_name: str) -> int:
    for idx,item in enumerate(config["notebooks"]):
        if item["name"] == notebook_name:
            return int(item["id"])
            exists = True
        else:
            exists = False
    if exists == False:
        print("Notebook does not exist")
        exit()

def getPageFromName(config, notebook_id, page_name: str) -> int:
    for idx,item in enumerate(config["notebooks"][notebook_id]["pages"]):
        if item["name"] == page_name + ".md" or item["name"] == page_name:
            return int(item["id"])


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
            name = getUserInput("Give the notebook a name: ")
            createNotebook(config,name)
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
