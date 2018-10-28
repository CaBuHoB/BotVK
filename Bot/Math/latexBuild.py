import os

from latex import build_pdf


def createPDF(document, filePath, fileName):
    pdf = build_pdf(document)
    pdf.save_to(os.path.join(filePath, fileName))


def getPreamble():
    return (r"\documentclass{article}"
            r"\usepackage[left=20mm, top=20mm, right=15mm, bottom=20mm, nohead, footskip=10mm]{geometry}"
            r"\usepackage{amsmath}"
            r"\usepackage{amsfonts}"
            r"\usepackage{amssymb}"
            r"\usepackage{makeidx}"
            r"\usepackage{graphicx}"
            r"\usepackage{multicol}"
            r""
            r"\begin{document}")


def getEnd():
    return r"\end{document}"


def getCases(matrix, variable=None):
    str = r"\["
    if variable is not None:
        str += variable + r"="
    str = str + r"\begin{cases}"
    for strFromMatrix in matrix:
        str = str + strFromMatrix + r" \\"
    str = str + r"\end{cases}"
    return str + r"\]"
