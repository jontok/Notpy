import os
from markdown import markdown
from markdown_pdf import MarkdownPdf, Section
from modules.read_md import getCurrentMarkdown

def convertToPDF(work_dir, path):
    filename = path.split("/")[-1].split(".")[0]
    markdown_str = getCurrentMarkdown(path)
    pdf = MarkdownPdf(toc_level=2)
    pdf.add_section(Section(markdown_str))
    pdf.meta["title"] = "Render"
    if not os.path.isdir(work_dir + "/tmp"):
        os.mkdir(work_dir + "/tmp")
    pdf.save(work_dir + "/tmp/" + filename + ".pdf")
    print("Rendered " + work_dir + "/tmp/" + filename + ".pdf")
