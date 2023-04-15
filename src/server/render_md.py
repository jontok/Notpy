from markdown import markdown

def renderMarkdown(markdown_str):
    return markdown(markdown_str, extensions=['nl2br', 'fenced_code'])