import os
import webbrowser
from pathlib import Path
from modules.render_md import convertToPDF
from modules.read_md import getCurrentMarkdown
from modules.notebook import listNotebook, listPages, getNotebookPage, getUserInput

def cliShowRenderMarkdown(work_dir, md_file_path):
    convertToPDF(work_dir, md_file_path)

def showRenderedMarkdown(work_dir,config):
    listNotebook(config)
    notebook_id = getUserInput("Select a notebook id: ", "int")
    listPages(config, notebook_id)
    page_id = getUserInput("Select a page id: ", "int")
    path_relativ = getNotebookPage(config, notebook_id, page_id)
    path = work_dir + path_relativ
    
    if os.path.exists(path):
        convertToPDF(work_dir, path)
        webbrowser.open_new_tab(work_dir + "/tmp/file.pdf")