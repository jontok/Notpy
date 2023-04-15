from client.edit_md import *
from client.show_md import *
from client.configure import editConfig
import os

# Temp VArs
work_dir = "/home/jt/Documents/Projects/Notpy/notpyFiles/"
file_path = work_dir + 'README.md'

def showHelp():
    print(
        "Notpy - Notetaking companion"
        "dasdad"
        )

def main():
    user_input = str(input("What do you want to do? "))
    match user_input:
        case "edit":
            editFile(work_dir)
        case "restart":
            os.execl(sys.argv[0], sys.argv)
        case "show":
            showRenderedMarkdown(work_dir)
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
    while True:
        main()