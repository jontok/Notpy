def getCurrentMarkdown(file_path):
    with open(file_path, 'r', encoding="utf-8") as open_file:
        current_markdown = open_file.read()

    return current_markdown