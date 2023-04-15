from os import system as sys
from server.show_md import createHTML
from client.notebook import listNotebook, listPages, getNotebookPage

def editFile(config,work_dir):
    listNotebook(config)
    notebook_id = input("Select a notebook: ")
    listPages(config, notebook_id)
    path_relativ = getNotebookPage(config, notebook_id)
    path = work_dir + path_relativ
    sys("nvim " + path)
    createHTML(work_dir, path)
    