import time

# replacement strings
WINDOWS_LINE_ENDING = str('\r\n')
UNIX_LINE_ENDING = str('\n')


def getCurrentMarkdown(file_path):
    with open(file_path, 'r', encoding="utf-8") as open_file:
        current_markdown = open_file.read()

    return current_markdown