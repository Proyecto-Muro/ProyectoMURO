import os


# To do list:
# Finish the solution page generator (add to dic)
# Add the generator for images
# Create a generator for ISL pages once it is needed
# Generate text for all high-level pages, and all folder pages


# This is the main function used for the generator. It replaces 
# text where needed in a template. 
def replace_all(text, dic): 
    for i, j in dic.items():
        text = text.replace(str(i), str(j))
    return text


# The fourth* entry in the dict is for years that need to be omitted.
# The third entry is the last year the contest took place
contestinfo = [
    ["IMO", 1959, 2022, [1980]],
    ["OMCC", 1999, 2021, []],
    ["OMM", 1987, 2021, []],
    ["EGMO", 2012, 2022, []],
    ["OIM", 1985, 2021, [1986]],
]

# define all problems from /concursos/contest/[year]/enunciados

def htmlproblems(contestname, year, ismax=False, ismin=False):

    # Declare the problems, will be set as empty if problem does not exist

    ProblemsList = []
    Problem = ""
    ProblemPosition = "1"
    dic = {
        "[Enunciadoproblema]": str(Problem),
        "[concurso]": str(contestname),
        "[año]": str(year),
        "[numproblema]": str(ProblemPosition),
        "[añoantes]": r'<a href="./../' + str(year - 1) + r'">◄</a>',
        "[añodespues]": r'<a href="./../' + str(year + 1) + r'">►</a>'
    }

    # This is to remove the arrows for first and last years.
    if ismax:
        dic["[añodespues]"]="" 
    if ismin:
        dic["[añoantes]"]=""


    Plist = os.listdir("./concursos/%s/%s/enunciados" % (contestname, year))
    Plist.sort()
    for i in Plist:
        if i[0] != ".":
            enunciado = "[Enunciado" + str(i[:-4]) + "]"
            dic[enunciado] = open("./concursos/%s/%s/enunciados/%s.tex" % (contestname, year, i[:-4])).read()
            ProblemsList.append(dic[enunciado])
            open("./concursos/%s/%s/enunciados/%s.tex" % (contestname, year, i[:-4])).close()
            # remember to do the same thing for solution pages

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


# Generates links for each year, to be used in contestindex pages

def GenerateYearLinks(year_start, year_end, exception_list):
    text = ''
    for i in range(year_end, year_start - 1, -1):
        if i in exception_list: # For contests that did not take place
            text += r"<h3><a href=./%s>%s</a>*</h3>" % (i, i)
        else:
            text += r"<h3><a href=./%s>%s</a></h3>" % (i, i)
    return text




def ReloadContestText(): # Writes contest information into main page, adds links for each year

    indexraw = open("generator/formats/contest-index.txt", "r").read()  # this is the format
    # We need a text and format for each contest.
    for i in contestinfo:
        yearRefs = GenerateYearLinks(i[1], i[2], i[3]) # Adds each link 
        concurso = i[0]
        contestText = open("generator/texts/%s.txt" % concurso, "r").read() 
        dic = {
            "[concurso]": concurso,
            "[yearlinks]": yearRefs,  # yearlinks must come from a list from each contest, and generate
            "[contestText]": contestText,
        }
        index = replace_all(indexraw, dic)
        with open("ProyectoMURO/public_html/%s/index.html" % concurso, "w") as f:
            f.write(index)
        open("generator/texts/%s.txt" % concurso).close()

    open("generator/formats/contest-index.txt").close()


def GenerateOthers(): # Generates pages from pageslist file
    from pageslist import pages_list
    with open("generator/formats/normal-page.txt", "r") as pagecontentraw:
        for i in pages_list:
            pagename = i[0]
            with open("generator/texts/%s.txt" % pagename, "r") as contestText:
                dic = {
                    "[HrefPag]": i[2],
                    "[TituloPag]": i[1],  # yearlinks must come from a list from each contest, and generate
                    "[TextoPag]": contestText,
                }
                pagecontent = replace_all(pagecontentraw, dic)
                if i[3] == 2:
                    with open("ProyectoMURO/public_html/%s/index.html" % pagename, "w") as f:
                        f.write(pagecontent)
                if i[3] == 1:
                    with open("ProyectoMURO/public_html/%s.html" % pagename, "w") as f:
                        f.write(pagecontent)

    # Generate all high-level pages, and all folder pages


def ReloadPages():
    # Reload Problem and Solution Pages
    for contest in contestinfo:
        for year in range(contest[1], contest[2]+1):
            if year not in contest[3]: # If the year did take place, generate the page
                htmlproblems(contest[0], year, year==contest[2], year==contest[1]) # Uses == to check if it is the first or last year.
            else:
                # Add a page: Contest did not take place said year.
                
                pass

    # Reload Contest Indexes, including text
    ReloadContestText()
