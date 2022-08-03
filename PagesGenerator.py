import os

# To do list:
# Finish the solution page generator (add to dic)
# Add the generator for images 
# Create a generator for ISL pages once it is needed
# Generate text for all high-level pages, and all folder pages

# ---------------------------------------------------------------------------------------------------------------------
# contestinfo: This list has information on each contest. 
# Format: [contest name (str), first contest year (int), last contest year (int), years omitted (list)]

contestinfo = [
    ["IMO", 1959, 2022, [1980]],
    ["OMCC", 1999, 2021, []],
    ["OMM", 1987, 2021, []],
    ["EGMO", 2012, 2022, []],
    ["OIM", 1985, 2021, [1986]],
    # ["ISL", 1998, 2021, []],
    ["APMO", 1989, 2022, []],
    ["RMM", 2008, 2021, []],
    ["PAGMO", 2021, 2021, []]
    # ["OMMFem", 2021, 2021, []]
]

# ---------------------------------------------------------------------------------------------------------------------
# Replace_all
# This is the main function used for the generator. It replaces 
# text where needed in a template. 

def replace_all(text, dic): 
    for i, j in dic.items():
        text = str(text).replace(str(i), str(j))
    return text

# ---------------------------------------------------------------------------------------------------------------------
# GenProbDiv
# Generates the section of the html used for showing an individual problem

def GenProbDiv(pnum):
    problemdiv = '''<h3><a href="./p{0}.html">Problema {0}</a></h3>\n
    <div class="alert-secondary alert">\n[Enunciado{0}]\n</div>\n'''.format(pnum)
    return str(problemdiv)

# ---------------------------------------------------------------------------------------------------------------------
# htmlproblems
# This function converts all .tex files in the directory to .html files with the appropriate format.

def htmlproblems(contestname, year, ismax=False, ismin=False):

    # Declare the problems' info, will be set as empty if problem does not exist

    ProblemsList = []
    ProblemText = ""
    ProblemPosition = "1"
    SolProb = ""
    dic = {
        "[Enunciadoproblema]": str(ProblemText),
        "[concurso]": str(contestname),
        "[año]": str(year),
        "[numproblema]": str(ProblemPosition),
        "[añoantes]": r'<a href="./../' + str(year - 1) + r'">◄</a>',
        "[añodespues]": r'<a href="./../' + str(year + 1) + r'">►</a>',
        "[SolucionProblema]": SolProb
    }

    # This is to remove the arrows for first and last years.
    if ismax:
        dic["[añodespues]"]="" 
    if ismin:
        dic["[añoantes]"]=""

    # -----------------------------------------------------------------------------------------------------------------
    # This section adds the problem statements to the dictionary

    PlistDot = os.listdir("concursos/%s/%s/enunciados" % (contestname, year))
    PlistDot.sort()
    Plist = []
    for i in PlistDot: # To avoid dotfiles like .DS_Store
        if i[0]!= ".":
            Plist.append(i)

    for i in Plist:

        # Creates [Enunciado_i] and adds enties to dict
        enunciado = "[Enunciado" + str(i[:-4]) + "]" 
        EnunciadoProblema = open("concursos/%s/%s/enunciados/%s.tex" % (contestname, year, i[:-4]), "r").read()
        dic[enunciado] = EnunciadoProblema
        ProblemsList.append(dic[enunciado]) # Add to ProblemsList for later use

    # -----------------------------------------------------------------------------------------------------------------
    # Year index creation

    # Copy file index.txt as a variable
    indexraw = open("generator/formats/year-index.txt", "r").read()

    # Here we create a dummy dict to add the number of problems, use GenProbDiv
    # This is to account for contests with different number of problems

    enunciadostring = ""
    for pnum in range(len(Plist)):
        enunciadostring += GenProbDiv(pnum + 1)
    enunciadosdict = {"[Enunciados]": enunciadostring}

    index1 = replace_all(indexraw, enunciadosdict)

    # Now we can replace again with the correct number of problems
    index2 = replace_all(index1, dic)

    # Write the complete file onto index.html
    indexlink = "ProyectoMURO/public_html/{0}/{1}/index.html".format(str(contestname),str(year))
    with open(indexlink, "w") as f:
        f.write(index2)

    # -------------------------------------------------------------------------------------------------------------
    # Individual problem and solution pages creation

    for pnum in range(len(Plist)):

        # Image check
        img = 0
        pstring = str(int(year) % 100) + contestname + str(pnum + 1)
        if pstring in os.listdir("concursos/asy-imgs"):
            # With this variable, we add images to text
            img = 1

        # Open problem format, replace with problem
        problempageraw = open("generator/formats/problem-page.txt", "r").read()

        dic["[Enunciadoproblema]"] = str(ProblemsList[pnum])
        if img == 1:
            pass
            #dic["[Enunciadoproblema]"] += # Agregar link imagen
            # Agregar imagen a /public_html/images/asy/
        dic["[numproblema]"] = str(pnum + 1)
        problempage = replace_all(problempageraw, dic)

        # Create link to add to file, write
        linkprob = "ProyectoMURO/public_html/{0}/{1}/p{2}.html".format(str(contestname), str(year), str(pnum + 1))
        with open(linkprob, "w") as f:
            f.write(problempage)

        # Import content
        SolucionProblema = open("./concursos/%s/%s/soluciones/%s.tex" % (contestname, str(year), str(pnum + 1)), "r").read()
        if SolucionProblema !="":
            dic["[SolucionProblema]"] = SolucionProblema
        else:
            # If empty add empty format
            dic["[SolucionProblema]"] = open("generator/texts/emptysol.txt", "r").read()

        # Open format, replace all content
        solutionpageraw = open("generator/formats/solution-page.txt", "r").read()
        solutionpage = replace_all(solutionpageraw, dic)

        # Create link to add file, write
        linksol = "ProyectoMURO/public_html/{0}/{1}/sol{2}.html".format(str(contestname), str(year), str(pnum + 1))
        with open(linksol, "w") as g:
            g.write(solutionpage)

# ---------------------------------------------------------------------------------------------------------------------
# GenerateYearLinks
# Generates links for each year, to be used in contestindex pages

def GenerateYearLinks(year_start, year_end, exception_list):

    text = ''

    for i in range(year_end, year_start - 1, -1):

        if i in exception_list: # For contests that did not take place
            text += "<h3><a href=./{0}>{0}</a>*</h3>".format(i)

        else:
            text += "<h3><a href=./{0}>{0}</a></h3>".format(i)

    return text

# ---------------------------------------------------------------------------------------------------------------------
# ReloadContestText
# Writes contest information into main pages, adds links for each year

def ReloadContestText():

    for i in contestinfo:

        yearRefs = GenerateYearLinks(i[1], i[2], i[3]) # Links for each year
        concurso = i[0] # Checks which contest is used

        contestText = open("generator/texts/%s.txt" % concurso, "r").read()

        dic = {
            "[concurso]": concurso,
            "[yearlinks]": yearRefs,  # yearlinks must come from a list from each contest, and generate
            "[contestText]": contestText,
            "[NotaOmitido]": ""
        }

        # Add note at bottom if a contest year was ommited
        if len(i[3]) != 0:
            dic["[NotaOmitido]"]="<p><i>Nota: </i> El concurso no se llevó a cabo en los años marcados con *.</p>"

        # Replace text
        indexraw = open("generator/formats/contest-index.txt", "r").read()
        index = replace_all(indexraw, dic) # This is the format, gets replaced with dic

        with open("ProyectoMURO/public_html/%s/index.html" % concurso, "w") as f:
            f.write(index) # Writes the page onto html file

# ---------------------------------------------------------------------------------------------------------------------
# ReloadOthers 
# Generates pages from pageslist.py file

def ReloadOthers(): 

    from pageslist import pages_list

    pageformat = open("generator/formats/normal-page.txt", "r").read() # Imports format
    for i in pages_list:
        pagename = i[0]
        pagecontent = open("generator/texts/%s.txt" % pagename, "r").read()
        dic = {
            "[HrefPag]": i[2],
            "[TituloPag]": i[1],
            "[TextoPag]": pagecontent,
        }
        pagehtml = replace_all(pageformat, dic)
        if i[3] == 2:
            with open("ProyectoMURO/public_html/%s/index.html" % pagename, "w") as f:
                f.write(pagehtml)
        if i[3] == 1:
            with open("ProyectoMURO/public_html/%s.html" % pagename, "w") as f:
                f.write(pagehtml)

        # TODO: Generate all high-level pages, and all folder pages


# ---------------------------------------------------------------------------------------------------------------------
# ReloadPages
# Reloads all the pages in the website. 

def ReloadPages():

    # Reload Problem and Solution Pages
    for contest in contestinfo:
        for year in range(contest[1], contest[2]+1):
            if year not in contest[3]: # If the year did take place, generate the page
                # Uses == to check if it is the first or last year.
                htmlproblems(contest[0], year, year==contest[2], year==contest[1]) 
            else:
                # Add a page: Contest did not take place said year.

                pass

    # Reload Contest Indexes, including text
    ReloadContestText()

    # Reload main pages content 
    ReloadOthers()
