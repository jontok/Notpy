import os
from server.render_md import *
from server.read_md import *
from client.notebook import listNotebook, listPages, getNotebookPage
import webbrowser

def createHTML(work_dir, md_file_path):
    if not os.path.exists(work_dir + "/tmp"):
        os.mkdir(work_dir + "/tmp")
    with open(work_dir + "/tmp/render.html", "w") as render_file:
        render_file.write(renderMarkdown(getCurrentMarkdown(md_file_path)))

def showRenderedMarkdown(work_dir,config):
    listNotebook(config)
    notebook_id = input("Select a notebook: ")
    listPages(config, notebook_id)
    path_relativ = getNotebookPage(config, notebook_id)
    path = work_dir + path_relativ
    print(os.path.exists(path))
    if os.path.exists(path):
        createHTML(work_dir, path)
        webbrowser.open_new_tab(work_dir + "/tmp/render.html")