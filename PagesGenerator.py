import os


def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(str(i), str(j))
    return text


# define all problems from /concursos/contest/[year]/enunciados

def htmlproblems(contestname, year):
    # define the problems, set as empty if problem does not exist
    ProblemsList = []
    Problem = ""
    ProblemPosition = "1"
    dic = {
        "[Enunciadoproblema]": str(Problem),
        "[concurso]": str(contestname),
        "[año]": str(year),
        "[numproblema]": str(ProblemPosition)
    }
    pcount = 0
    Plist = os.listdir("./concursos/%s/%s/enunciados" % (contestname, year))
    Plist.sort()
    for i in Plist:
        if i[0] != ".":
            enunciado = "[Enunciado" + str(i[:-4]) + "]"
            dic[enunciado] = open("./concursos/%s/%s/enunciados/%s.tex" % (contestname, year, i[:-4])).read()
            ProblemsList.append(dic[enunciado])
            open("./concursos/%s/%s/enunciados/%s.tex" % (contestname, year, i[:-4])).close()
            # remember to do the same thing for solution pages

    numproblems = len(ProblemsList)

    # YEAR FILE CREATION
    # copy file index.txt as a variable
    indexraw = open("generator/formats/year-index.txt", "r").read()
    # replace variables
    index = replace_all(indexraw, dic)
    # write onto index.html
    with open("ProyectoMURO/public_html/" + str(contestname) + "/" + str(year) + "/" + "index.html", "w") as f:
        f.write(index)

    for i in range(6):
        img = 0
        # don't forget to check for images
        pstring = str(int(year) % 100) + contestname + str(i)
        if pstring in os.listdir("./aops-script/asy-imgs"):
            # do the thing (images)
            img = 1
        # create file problemindex.html, replace
        problempageraw = open("generator/formats/problem-page.txt", "r").read()
        # replace variables
        # define Problem and ProblemPosition in dict
        dic["[Enunciadoproblema]"] = str(ProblemsList[i])
        dic["[numproblema]"] = str(i + 1)
        problempage = replace_all(problempageraw, dic)
        with open("ProyectoMURO/public_html/" + str(contestname) + "/" + str(year) + "/" + "p" + str(i + 1) + ".html",
                  "w") as f:
            f.write(problempage)
        # create file sol_i.html
        solutionpageraw = open("generator/formats/solution-page.txt", "r").read()
        solutionpage = replace_all(solutionpageraw, dic)
        with open("ProyectoMURO/public_html/" + str(contestname) + "/" + str(year) + "/" + "sol" + str(i + 1) + ".html",
                  "w") as g:
            g.write(solutionpage)
        open("generator/formats/problem-page.txt", "r").close()
        open("generator/formats/solution-page.txt", "r").close()


def GenerateYearLinks(year_start, year_end):
    text = ''
    for i in range(year_start, year_end + 1):
        text += r"<h3><a href=./%s>%s</a></h3>\n" % (i, i)
    return text


def ReloadContestText():
    from contestinfo import contestList
    indexraw = open("/generator/formats/contest-index.txt").read()  # this is the format
    # We need a text and format for each contest.
    for i in contestList:
        yearRefs = GenerateYearLinks(i[1], 1[2])
        concurso = i[0]
        contestText = open("generator/texts/%s.txt" % concurso).read()
        dic = {
            "[concurso]": concurso,
            "[yearlinks]": yearRefs,  # yearlinks must come from a list from each contest, and generate
            "[contestText]": contestText,
        }
        index = replace_all(indexraw, dic)
        with open("ProyectoMURO/public_html/%s/index.html" % concurso) as f:
            f.write(index)
        open("generator/texts/%s.txt" % concurso).close()

    open("/generator/formats/contest-index.txt").close()


def ReloadPages():
    # Reload Problem and Solution Pages
    contestinfo = [
        ["IMO", 1959],
        ["OMCC", 1999],
        ["OMM", 1987],
        ["EGMO", 2012],
        ["OIM", 1985],
        ["OMCC", 1999]
    ]
    for i in contestinfo:
        for j in range(i[1], 2022):
            htmlproblems(i[0], j)

    # Reload Contest Indexes, including text
    ReloadContestText()
