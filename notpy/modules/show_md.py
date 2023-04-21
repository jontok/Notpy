import os
import webbrowser
from pathlib import Path
from modules.render_md import renderMarkdown
from modules.read_md import getCurrentMarkdown
from modules.notebook import listNotebook, listPages, getNotebookPage, getUserInput


def createHTML(work_dir, md_file_path):
    if not os.path.exists(work_dir + "/tmp"):
        os.mkdir(work_dir + "/tmp")
    with open(work_dir + "/tmp/render.html", "w") as render_file:
        css_start   = '<!DOCTYPE html><html><head><link rel="stylesheet" type="text/css" href="' + str(Path.home()) + '/.config/notpy/styles.css"></head><body>\n'
        css_end     = '</body></html>'
        render_file.write(css_start + renderMarkdown(getCurrentMarkdown(md_file_path)) + css_end)

def cliShowRenderMarkdown(work_dir):
    webbrowser.open(work_dir + "/tmp/render.html")


def showRenderedMarkdown(work_dir,config):
    listNotebook(config)
    notebook_id = getUserInput("Select a notebook id: ", "int")
    listPages(config, notebook_id)
    page_id = getUserInput("Select a page id: ", "int")
    path_relativ = getNotebookPage(config, notebook_id, page_id)
    path = work_dir + path_relativ
    
    if os.path.exists(path):
        createHTML(work_dir, path)
        webbrowser.open_new_tab(work_dir + "/tmp/render.html")