from client.edit_md import *
from server.show_md import *
from client.configure import editConfig, getConfigFile
from client.notebook import notebooks
from pathlib import Path
import os

# Temp VArs
config_file = str(Path.home()) + "/.config/notpy/config.json"

def showHelp():
    print(
        "Notpy - Notetaking companion"
        "dasdad"
        )

def main():
    while True:
        config = getConfigFile(config_file)
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
                print("Nothing")
    #print(renderMarkdown(str(getCurrentMarkdown(file_path))))
    #return renderMarkdown(str(getCurrentMarkdown(file_path)))


if __name__ == "__main__":
    main()