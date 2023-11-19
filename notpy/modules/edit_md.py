import os
import texteditor
from os import system
from modules.configure import getDefaultEditor
from modules.notebook import listNotebook, listPages, getNotebookPage, getUserInput, createNotebook, createPage
from modules.show_md import convertToPDF

def editNewFile(config, file_path):
    parts = file_path.rsplit("/", 2)  # split by "/" from right to left, up to 2 times
    work_dir = "/".join(parts[:2]) + "/"
    editor = texteditor.get_editor()[0]
    if getDefaultEditor(config) != "":
        editor = getDefaultEditor(config)
    system(editor + " " + file_path)
    if os.path.exists(file_path):
        convertToPDF(work_dir, file_path)



def editFile(config,work_dir):
    create_new_nb = getUserInput("Use existing Notebook default: yes(Y/n): ")
    match create_new_nb:
        case "y" | "Y" | "yes":
            createNotebook(config)
        case "n" | "no":
            listNotebook(config)
            notebook_id = getUserInput("Select a notebook id: ", "int")
        case _:
            print("Not a valid input")

    create_new_pg = getUserInput("Use existing Notebook default: yes(Y/n): ")
    match create_new_pg:
        case "y" | "Y" | "yes":
            createPage(config)
        case "n" | "no":
            listPages(config, notebook_id)
            page_id = getUserInput("Select a page id: ", "int")
        case _:
            print("Not a valid input")
            
    listPages(config, notebook_id)
    page_id = getUserInput("Select a page id: ", "int")
    path_relativ = getNotebookPage(config, notebook_id, page_id)
    path = work_dir + path_relativ
    system("nvim " + path)
    convertToPDF(work_dir, path)
    