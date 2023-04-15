import os
from server.render_md import *
from server.read_md import *
import webbrowser

def createHTML(work_dir, md_file_path):
    
    with open(work_dir + "tmp/render.html", "w") as render_file:
        render_file.write(renderMarkdown(getCurrentMarkdown(md_file_path)))

def showRenderedMarkdown(work_dir):
    file = str(input("file name: "))
    path = work_dir + file + ".md"
    print(os.path.exists(path))
    if os.path.exists(path):
        createHTML(work_dir, path)
        webbrowser.open_new_tab(work_dir + "tmp/render.html")