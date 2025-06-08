import os
import shutil
import platform
import subprocess
from modules.configure import getDefaultEditor
from modules.notebook import listNotebook, listPages, getNotebookPage, getUserInput, createNotebook, createPage
from modules.show_md import convertToPDF

def get_default_editor():
    """Get default text editor based on environment and platform"""
    # Check environment variables first
    editor = os.environ.get('EDITOR') or os.environ.get('VISUAL')
    if editor and shutil.which(editor):
        return editor
    
    # Platform-specific defaults
    system_name = platform.system().lower()
    
    if system_name == "windows":
        editors = ["notepad++", "notepad", "code", "vim", "nano"]
    elif system_name == "darwin":  # macOS
        editors = ["code", "vim", "nano", "emacs", "gedit"]
    else:  # Linux and others
        editors = ["vim", "nano", "emacs", "gedit", "code", "kate"]
    
    # Find first available editor
    for editor in editors:
        if shutil.which(editor):
            return editor
    
    # Fallback
    return "vim" if system_name != "windows" else "notepad"

def editNewFile(config, file_path):
    # Security: Validate file_path is absolute and normalized
    file_path = os.path.abspath(file_path)
    work_dir = os.path.dirname(os.path.dirname(file_path))
    editor = get_default_editor()
    if getDefaultEditor(config) != "":
        editor = getDefaultEditor(config)
    
    # Security fix: Use subprocess.run() to prevent command injection
    try:
        subprocess.run([editor, file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error opening editor: {e}")
        return
    except FileNotFoundError:
        print(f"Editor '{editor}' not found")
        return
    
    if os.path.exists(file_path):
        convertToPDF(work_dir, file_path)



def editFile(config,work_dir):
    create_new_nb = getUserInput("Use existing Notebook default: yes(Y/n): ")
    if create_new_nb is None:
        return
        
    match create_new_nb:
        case "y" | "Y" | "yes":
            createNotebook(config)
        case "n" | "no":
            listNotebook(config)
            notebook_id = getUserInput("Select a notebook id: ", "int")
            if notebook_id is None:
                return
        case _:
            print("Not a valid input")

    create_new_pg = getUserInput("Use existing Notebook default: yes(Y/n): ")
    if create_new_pg is None:
        return
        
    match create_new_pg:
        case "y" | "Y" | "yes":
            createPage(config)
        case "n" | "no":
            listPages(config, notebook_id)
            page_id = getUserInput("Select a page id: ", "int")
            if page_id is None:
                return
        case _:
            print("Not a valid input")
            
    listPages(config, notebook_id)
    page_id = getUserInput("Select a page id: ", "int")
    if page_id is None:
        return
    path_relativ = getNotebookPage(config, notebook_id, page_id)
    
    # Security: Use os.path.join for safe path construction
    path = os.path.abspath(os.path.join(work_dir, path_relativ.lstrip("/")))
    
    # Security fix: Use subprocess.run() to prevent command injection
    try:
        subprocess.run(["nvim", path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error opening editor: {e}")
        return
    except FileNotFoundError:
        print("Editor 'nvim' not found")
        return
    
    convertToPDF(work_dir, path)
    