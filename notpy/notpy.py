import os
import sys
from pathlib import Path
sys.path.append((str(Path.home()) + "/.local/lib/python3.10/site-packages/notpy"))
from modules.edit_md import editFile
from modules.show_md import showRenderedMarkdown
from modules.configure import editConfig, getConfigFile
from modules.notebook import notebooks
from modules.commandline import cliMain



def showHelp():
    print(
        "Notpy - Notetaking companion"
        "dasdad"
        )

def main():
    config_file = str(Path.home()) + "/.config/notpy/config.json"
    while True:
        config = getConfigFile(config_file)
        if len(sys.argv) >= 2:
            cliMain(config, sys.argv)
            break
        
        print("\nNotpy options:")
        print("edit         - edit a Page")
        print("notebook     - add/delete Notebooks and pages")
        print("show         - Show page")
        print("help         - Shows info for Notpy")
        print("configure    - configure Notpy")
        print("exit         - exit notpy")
        
        work_dir = str(config["paths"]["homeDir"]) + str(config["paths"]["notebookDir"])
        user_input = str(input("What do you want to do? "))
        
        match user_input:
            case "edit":
                editFile(config,work_dir)
            case "restart":
                os.execl(sys.argv[0], sys.argv)
            case "show":
                showRenderedMarkdown(work_dir,config)
            case "notebook":
                notebooks(config_file)
            case "help":
                showHelp()
            case "configure":
                editConfig()
            case "exit":
                exit()
            case _:
                print("Not a valid argument")