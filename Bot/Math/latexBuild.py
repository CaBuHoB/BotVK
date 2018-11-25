import os

from latex import build_pdf


def createPDF(document, filePath, fileName):
    pdf = build_pdf(document, [], 'pdflatex')
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
            r"\usepackage[english,russian]{babel}"
            r""
            r"\begin{document}")


def getEnd():
    return r"\end{document}"


def getCases(matrix, variable=None):
    cases = r"\["
    if variable is not None:
        cases += variable + r"="
    cases = cases + r"\begin{cases}"
    for strFromMatrix in matrix:
        cases = cases + strFromMatrix + r" \\"
    cases = cases + r"\end{cases}"
    return cases + r"\]"


def getMinipageBegin(size=50, parindent=None):
    minipage = r"\begin{minipage}[t]{"
    minipage = minipage + str(size) + r"mm}"
    if parindent is not None:
        minipage = minipage + r"\parindent=" + str(parindent) + r"em"
    return minipage


def getMinipageEnd():
    return r"\end{minipage}"
