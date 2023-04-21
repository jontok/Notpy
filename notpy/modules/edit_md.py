import os
from os import system
from modules.notebook import listNotebook, listPages, getNotebookPage, getUserInput, createNotebook, createPage
from modules.show_md import createHTML

def editNewFile(file_path):
    parts = file_path.rsplit("/", 2)  # split by "/" from right to left, up to 2 times
    work_dir = "/".join(parts[:2]) + "/"
    system("nvim " + file_path)
    if os.path.exists(file_path):
        createHTML(work_dir, file_path)

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
    createHTML(work_dir, path)
    