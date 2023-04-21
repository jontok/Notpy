import os
import shutil
from pathlib import Path
from edit_md import editNewFile
from configure import editConfig, setConfigFile, generatePageObject
from notebook import (
    getNotebookFromName,
    getPageFromName,
    deleteObjectFromConfig,
    listNotebook,
    listPages,
    createNotebook,
    getUserInput
)
###################################################################
# CLI
###################################################################
config_file = str(Path.home()) + "/.config/notpy/config.json"


def cliShowHelp():
    print(str(cliShowHelp.__name__) + ' was not found!')


def cliListMethod(config, args):
    if len(args) <= 3:
        print(
            "Please use one of the options: " +
            "'notpy ls nb' or 'notpy ls pg [notebook]'"
        )
        exit()
    match args[2]:
        case "pg":
            notebook_id = args[3]
            try:
                notebook_id = int(notebook_id)
            except ValueError:
                if type(notebook_id) != int:
                    notebook_id = getNotebookFromName(config, notebook_id)

            listPages(config, int(notebook_id))

        case "nb":
            listNotebook(config)
        case _:
            print("Not a valid argument")


def cliEditMethod(config, args):
    if len(args) <= 4:
        print("Please provide a notebook name or id and a page name or id")
        exit()
    match args[2]:
        case "pg":
            notebook_id = args[3]
            try:
                notebook_id = int(notebook_id)
            except ValueError:
                if type(notebook_id) != int:
                    notebook_id = getNotebookFromName(config, notebook_id)

            page_id = args[4]
            try:
                page_id = int(page_id)  # try to convert x to an integer
            except ValueError:
                if type(page_id) != int:
                    page_id = getPageFromName(
                                config,
                                notebook_id,
                                str(page_id)
                            )

            try:
                pg_dir = config["notebooks"][notebook_id]["pages"][page_id]["name"]
            except:
                pg_dir      = args[4]
                if pg_dir[:3] == ".md":
                    pg_dir = pg_dir + ".md"
                config["notebooks"][notebook_id]["pages"].append(
                    generatePageObject(config, notebook_id, pg_dir)
                )
                setConfigFile(config_file, config)

            work_dir = config["paths"]["homeDir"] + config["paths"]["notebookDir"]
            nb_dir = config["notebooks"][notebook_id]["name"]
            path = work_dir + "/" + nb_dir + "/" + pg_dir
            
            editNewFile(path)
        
        case _:
            print("Not avalid argument")

def cliCreateMethod(config, args):
    match args[2]:
        case "pg":
            cliEditMethod(config, args)
        case "nb":
            notebook_id = args[3]
            try:
                notebook_id = str(notebook_id)  # try to convert x to an integer
            except ValueError:
                pass
            createNotebook(config, notebook_id)


def cliDeleteMethod(config, args):
    # User should always confirm before deleting a page or notebooks
    if not len(args) >=3:
        print("Please provide a notebook name or id and a page name or id")
        exit()
    match args[2]:
        case "pg":
            # get notebook ID as int
            notebook_id = args[3]
            try:
                notebook_id = int(notebook_id)  # try to convert x to an integer
            except ValueError:
                if type(notebook_id) != int:
                    notebook_id = getNotebookFromName(config, notebook_id)
            
            
            # get page ID as int
            page_id = args[4]
            try:
                page_id = int(page_id)  # try to convert x to an integer
            except ValueError:
                if type(page_id) != int:
                    page_id = getPageFromName(config, notebook_id, str(page_id))

            # generate path
            try:
                pg_dir      = config["notebooks"][notebook_id]["pages"][page_id]["name"]
            except:
                pg_dir      = args[4]
                if pg_dir[:3] == ".md":
                    pg_dir = pg_dir + ".md"
            work_dir    = config["paths"]["homeDir"] + config["paths"]["notebookDir"]
            nb_dir      = config["notebooks"][notebook_id]["name"]
            path        = work_dir + "/" + nb_dir + "/" + pg_dir
            
            # check if path exists
            if not os.path.exists(path):
                print("Page does not exist")
                exit()

            # Confirm and Delete page
            confirm_delete = getUserInput("Do you want to delete " + path + " (Y/n): ")
            match confirm_delete:
                case "y" | "Y":
                    deleteObjectFromConfig(config, config["notebooks"][notebook_id]["pages"], page_id)
                    os.remove(path)
                    print("Page deleted")
                case _:
                    print("Page not deleted")
                
        case "nb":
            # get notebook ID as int
            notebook_id = args[3]
            try:
                notebook_id = int(notebook_id)
                
            except ValueError:
                if type(notebook_id) != int:
                    notebook_id = getNotebookFromName(config, notebook_id)

    
            
            # set Notebook path
            work_dir    = config["paths"]["homeDir"] + config["paths"]["notebookDir"]
            nb_dir      = config["notebooks"][notebook_id]["name"]
            path        = work_dir + "/" + nb_dir

            # check if path exists
            if not os.path.exists(path):
                print("Page does not exist")
                exit()

            # Confirm and Delete page
            confirm_delete = getUserInput("Do you want to delete " + path + " (Y/n): ")
            match confirm_delete:
                case "y" | "Y":
                    deleteObjectFromConfig(config, config["notebooks"], notebook_id)
                    shutil.rmtree(path)
                    print("Notebook deleted")
                case _:
                    print("Notebook not deleted")

        
        case _:
            print("Not a valid argument")

def cliMain(config, args):
    match args[1]:
        case "console":
            print("Console")
        case "configure":
            editConfig()
        case "ls":
            cliListMethod(config, args)
        case "ed":
            cliEditMethod(config, args)
        case "create":
            cliCreateMethod(config, args)
        case "del":
            cliDeleteMethod(config, args)
        case "help" | "-h" | "--help":
            cliShowHelp()
        case _:
            print("Not a vaild argument")