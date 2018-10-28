from Bot.Math.latexBuild import getPreamble, getEnd, createPDF, getCases
import os


def createFileExtendedEuclideanAlgorithm(task, userID):
    if len(task) != 3:
        return "Неверные данные", None

    a = int(task[0])
    b = int(task[1])
    mod = int(task[2])

    latex = getPreamble()
    latex = latex + r"\begin{flushleft}"
    latex = latex + "$" + str(a) + "x=" + str(b) + "~mod~" + str(mod) + r"$ \\"
    latex = latex + "$" + str(a) + "x + " + str(mod) + "y = " + str(b) + r"$ \\"

    r = []
    x = []
    y = []
    k = []

    r.append(mod)
    x.append(0)
    y.append(1)
    k.append(None)
    latex = latex + getCases(["r_{-1}=" + str(r[0]), "x_{-1}=" + str(x[0]), "y_{-1}=" + str(y[0])])

    r.append(a)
    x.append(1)
    y.append(0)
    k.append(int(mod / a))
    latex = latex + getCases(["r_{0}=" + str(r[1]), "x_{0}=" + str(x[1]), "y_{0}=" + str(y[1]), "k_{0}=" + str(k[1])])

    i = 2
    while True:
        r.append(r[i - 2] - (r[i - 1] * k[i - 1]))
        x.append(x[i - 2] - (x[i - 1] * k[i - 1]))
        y.append(y[i - 2] - (y[i - 1] * k[i - 1]))
        k.append(int(r[i - 1] / r[i]))
        latex = latex + getCases(["r_{" + str(i - 1) + "}=" + str(r[i]), "x_{" + str(i - 1) + "}=" + str(x[i]),
                                  "y_{" + str(i - 1) + "}=" + str(y[i]), "k_{" + str(i - 1) + "}=" + str(k[i])])

        if r[i] == 1:
            break
        i = i + 1

    x = x[i]
    y = y[i]
    latex = latex + "$" + str(a) + "\cdot" + str(x) + " + " + str(mod) + "\cdot" + str(y) + " = " + r"1$ \\"
    x = x * b
    y = y * b
    latex = latex + "$" + str(a) + "\cdot" + str(x) + " + " + str(mod) + "\cdot" + str(y) + " = " + str(b) + r"$ \\"
    x = x % mod
    y = y % mod
    latex = latex + "$" + str(a) + "\cdot" + str(x) + " + " + str(mod) + "\cdot" + str(y) + " = " + str(b) + r"$ \\"

    latex = latex + "Answer: $x$ = " + "$" + str(x) + "~mod~" + str(mod) + r"$ \\"
    # latex = latex + "Надо ли $y$? Ну, лишним не будет: $y$ = " + "$" + str(y) + "~mod~" + str(mod) + r"$"

    latex = latex + r"\end{flushleft}" + getEnd()
    name = str(userID) + 'EEA.pdf'
    createPDF(latex, '/tmp', name)
    return None, os.path.join('/tmp', name)
