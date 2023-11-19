import os
from os.path import exists
import shutil
import pkg_resources
from pathlib import Path
from modules.edit_md import editNewFile
from modules.show_md import cliShowRenderMarkdown
from modules.render_md import convertToPDF
from modules.configure import editConfig, setConfigFile, getBaseConfig, generatePageObject, setDefaultEditor
from modules.notebook import (
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
    print("NotPy")
    print()
    print("Usage: notpy [options] [arguments]")
    print()
    print("Run NotPy: A simple note-taking CLI tool")
    print()
    print("Options:")
    print("  -h, --help         Print this usage message")
    print("  -v, --version      Print the version")
    print()
    print("Commands:")
    print("  The following commands are available:")
    print("  configure                      - configure Notpy")
    print("  ls nb                          - list all notebooks")
    print("  ls pg [notebook]               - list all pages in a notebook")
    print("  show [notebook] [page]         - render page to pdf")
    print("  edit pg [notebook] [page]      - edit a page in a notebook")
    print("  create nb [notebook]           - create a new notebook")
    print("  create pg [notebook] [page]    - create a new page in a notebook")
    print("  delete nb [notebook]           - delete a notebook")
    print("  delete pg [notebook] [page]    - delete a page from a notebook")


def cliListMethod(config, args):
    if len(args) <= 2:
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
            
            if 5 < len(args):
                if args[5] == "-y":
                    os.mknod(path)
                    config["notebooks"][notebook_id]["pages"].append(
                        generatePageObject(config, notebook_id, pg_dir)
                    )
                    setConfigFile(config_file, config)
                    exit()
            else:
                editNewFile(config, path)
        
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

            
            if 5 < len(args):
                if args[5] == "-y":
                    deleteObjectFromConfig(config, config["notebooks"][notebook_id]["pages"], page_id)
                    os.remove(path)
                    print("Page deleted")
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

            if 4 < len(args):
                if args[4] == "-y":
                    deleteObjectFromConfig(config, config["notebooks"], notebook_id)
                    shutil.rmtree(path)
                    print("Notebook deleted")
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

def setDefaultConfig():
    home = str(Path.home())
    path = home + "/.config/notpy"
    config_file = path + "/config.json"
    config = getBaseConfig()
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(config_file):
        with open(config_file, 'w'): pass
    homeDir = config["paths"]["homeDir"]
    if homeDir == "":
        config["paths"]["homeDir"] = str(Path.home())
    notebookPath = str(config["paths"]["homeDir"]) + str(config["paths"]["notebookDir"])
    if not os.path.exists(notebookPath):
        os.mkdir(notebookPath)
    setConfigFile(config_file, config)
    exit()

def cliEditConfig(config, args):
    if args[1] == "configure" and len(args)-1 == 1:
        editConfig()
        exit()

    match args[2]:
        case "editor":
            print(args[2])
            editor_str = str(args[3])
            config["paths"]["defaultEditor"] = editor_str
            setConfigFile(config_file, config)
        case "default":
            try:
                if args[3] == "-y":
                    setDefaultConfig()
            except IndexError:
                confirm = str(input("This will overwrite your current config and could break Notpy, continue anyway (Y/n): "))
                match confirm:
                    case "Y" | "y" | "yes":
                        setDefaultConfig()
                    case "N" | "n" | "no":
                        exit()
                    case _:
                        print("Not a valid argument")
        case "help":
            print("  notpy configure [command] [options]")
            print("  The following commands are available:")
            print("  editor                      - set default editor")
            print("  default                     - set default configuration (made for CI/CD) -y flag for non-interactiv")
            
        case _:
            print("Not a valid argument")
 
def cliShowPage(config, args):
    notebook_id = args[2]
    try:
        notebook_id = int(notebook_id)
        
    except ValueError:
        if type(notebook_id) != int:
            notebook_id = getNotebookFromName(config, notebook_id)
    pg_dir = args[3]
    work_dir    = config["paths"]["homeDir"] + config["paths"]["notebookDir"]
    nb_dir      = work_dir + "/" + config["notebooks"][notebook_id]["name"]
    path        = nb_dir + "/" + pg_dir
    cliShowRenderMarkdown(nb_dir, path)

def cliMain(config, args):
    match args[1]:
        case "console":
            print("Console")          
        case "configure":
            cliEditConfig(config, args)
        case "ls":
            cliListMethod(config, args)
        case "edit":
            cliEditMethod(config, args)
        case "create":
            cliCreateMethod(config, args)
        case "delete":
            cliDeleteMethod(config, args)
        case "show":
            cliShowPage(config, args)
        case "help" | "-h" | "--help":
            cliShowHelp()
        case "version" | "-v" | "--version":
            print(f"Notpy version {pkg_resources.get_distribution('notpy').version}")
        case _:
            print("Not a vaild argument")
