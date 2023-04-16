from os import system
from server.show_md import createHTML
from client.notebook import listNotebook, listPages, getNotebookPage, getUserInput, createNotebook, createPage

def editNewFile(file_path):
    system("nvim " + path)
    createHTML(work_dir, path)

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
    