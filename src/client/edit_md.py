from os import system as sys
from client.show_md import createHTML

def editFile(work_dir):
    file = str(input("file name: "))
    path = work_dir + file + ".md"
    sys("nvim " + path)
    createHTML(work_dir, path)
    