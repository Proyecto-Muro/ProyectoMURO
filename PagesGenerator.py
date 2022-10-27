# To do list:
# Finish the solution page generator (add to dic)
# Adjust generator for IWYMIC pages

# ---------------------------------------------------------------------------------------------------------------------
# Imports


from os import listdir
from info import pages_list, contestinfo, islproblems

# Formats and lists

asyimgs = listdir("ProyectoMURO/public_html/images/asy-imgs")

indexrawcontest = open("generator/formats/contest-index.txt", "r").read() 
indexrawyear = open("generator/formats/year-index.txt", "r").read()
ommebyearindex = open("generator/texts/ommebyearindex.txt", "r").read()
islyearindex = open("generator/texts/islyearindex.txt", "r").read()
problempageraw = open("generator/formats/problem-page.txt", "r").read()
emptysoltext = open("generator/texts/emptysol.txt", "r").read()
solutionpageraw = open("generator/formats/solution-page.txt", "r").read()
pageformat = open("generator/formats/normal-page.txt", "r").read() 



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
    <div class="alert-secondary alert">\n[Enunciado{0}]\n</div>\n
    <button class="button" onclick=
    "copyEvent(`
    [EnunciadoLatex{0}]
    `)"
    >Copiar LaTeX</button>
    <hr> '''.format(pnum)
    return str(problemdiv)

def GenProbDivISL(problem):
    puid = ""
    if problem in ["A1", "C1", "G1", "N1"]:
        puid = problem[0]
    problemdiv = '''<h3><a href="./{0}.html">{0}</a></h3>\n
    <div class="alert-secondary alert" id=\"'''.format(problem) + puid + '''">\n[Enunciado{0}]\n</div>\n
    <button class="button" onclick=
    "copyEvent(`
    [EnunciadoLatex{0}]
    `)"
    >Copiar LaTeX</button>
     '''.format(problem)
    if puid not in ["", "A"]:
        problemdiv = "<hr>" + problemdiv

    return str(problemdiv)

def GenProbDivOMMEB(problem):
    problemname = ""
    puid = ""
    for i in problem:
        if i=="n":
            problemname += "Nivel "
        elif i=="e":
            problemname += " Equipos "
        elif i=="p":
            problemname += " Problema "
        else:
            problemname += i
    if problem == "n1p1":
        puid = "Nivel1"
    elif problem == "n1e1":
        puid = "Nivel1Equipos"
    elif problem == "n2p1":
        puid = "Nivel2"
    elif problem == "n2e1":
        puid = "Nivel2Equipos"
    elif problem == "n3p1":
        puid = "Nivel3"
    elif problem == "n3e1":
        puid = "Nivel3Equipos"

    problemdiv = '''<h3><a href="./{0}.html">{1}</a></h3>\n
    <div class="alert-secondary alert" id=\"'''.format(problem, problemname) + puid + '''\">\n[Enunciado{0}]\n</div>\n
    <button class="button" onclick=
    "copyEvent(`
    [EnunciadoLatex{0}]
    `)"
    >Copiar LaTeX</button>
    '''.format(problem, problemname)
    if puid not in ["", "Nivel1"]:
        problemdiv = "<hr>" + problemdiv
    return str(problemdiv)

# ---------------------------------------------------------------------------------------------------------------------
# htmlproblems
# This function converts all .tex files in the directory to .html files with the appropriate format.

def htmlproblems(contestname, year, ismax=False, ismin=False):

    pagecount = 0

    # Declare the problems' info, will be set as empty if problem does not exist

    ProblemsList = []
    ProblemsListLatex = []
    dic = {
        "[Enunciadoproblema]": "",
        "[EnunciadoLatexproblema]": "",
        "[concurso]": str(contestname),
        "[año]": str(year),
        "[numproblema]": "1",
        "[añoantes]": r'<a href="./../' + str(year - 1) + r'">◄</a>',
        "[añodespues]": r'<a href="./../' + str(year + 1) + r'">►</a>',
        "[SolucionProblema]": "",
        "[YearIndexExtra]": ""
    }

    # This is to remove the arrows for first and last years.
    if ismax:
        dic["[añodespues]"]="" 
    if ismin:
        dic["[añoantes]"]=""

    # -----------------------------------------------------------------------------------------------------------------
    # This section adds the problem statements to the dictionary

    PlistDot = listdir("concursos/%s/%s/enunciados" % (contestname, year))
    PlistDot.sort()
    Plist = []
    for i in PlistDot: # To avoid dotfiles like .DS_Store
        if i[0]!= ".":
            Plist.append(str(i)[:-4])

    # Contest check

    # Make list of problems: Level 1-3, Problem 1-15, Team 1-8. Example: n3p12, n1e5
    if contestname == "OMMEB":
        Plist = []
        for i in range(1,4):
            for j in range(1, 16):
                Plist.append("n%sp%s"%(i,j))
            for j in range(1, 9):
                Plist.append("n%se%s"%(i,j))

    # Make list of ISL problems
    if contestname == "ISL":
        Plist = []
        letters = ["A", "C", "G", "N"]
        areas = islproblems[year - 1998]
        for i in range(4): 
            for j in range(areas[i]):
                Plist.append(letters[i]+str(j+1))

    for problem in Plist:

        # Creates [Enunciado_i]
        enunciado = "[Enunciado" + problem + "]" 
        EnunciadoProblema = open("concursos/%s/%s/enunciados/%s.tex" % (contestname, year, problem), "r").read()

        # Creates [EnunciadoLatex_i]
        enunciadolatex = "[EnunciadoLatex" + problem + "]" 
        EnunciadoLatexProblema = open("concursostex/%s/%s/enunciados/%s.tex" % (contestname, year, problem), "r").read()

        # Hay que duplicar los \ en los enunciados porque crean errores con los caracteres al copiarse
        TempEnunciado = ""

        for i in EnunciadoLatexProblema:
            if i == "\\": 
                TempEnunciado += i + i
            else:
                TempEnunciado += i

        EnunciadoLatexProblema = TempEnunciado

        # Image check
        yearmod100 = str(int(year) % 100)
        if len(yearmod100)==1:
            yearmod100 = "0" + yearmod100
        pstring = yearmod100 + contestname + problem + ".png"
        if pstring in asyimgs:
            # Add image html to problem 
            # print("Image found:" + pstring)
            imgstr = "\n"+r'<p>' + r'<img src="/images/asy-imgs/{0}" alt="{0}" height="100" class="center"></p>'.format(pstring)
            EnunciadoProblema += imgstr
            
        # Add entries to dict
        dic[enunciado] = EnunciadoProblema
        dic[enunciadolatex] = EnunciadoLatexProblema

        ProblemsList.append(dic[enunciado]) # Add to ProblemsList for later use
        ProblemsListLatex.append(dic[enunciadolatex])

    # -----------------------------------------------------------------------------------------------------------------
    # Year index creation

    # Here we create a dummy dict to add the number of problems, use GenProbDiv
    # This is to account for contests with different number of problems

    if contestname not in ["ISL", "OMMEB"]: # OMMEB/ISL check
        enunciadostring = ""
        for pnum in range(len(Plist)):
            enunciadostring += GenProbDiv(pnum + 1)
        enunciadosdict = {"[Enunciados]": enunciadostring}

    elif contestname == "OMMEB": #OMMEB
        enunciadostring = ""
        for problem in Plist:
            enunciadostring += GenProbDivOMMEB(problem)
        enunciadosdict = {"[Enunciados]": enunciadostring}

        dic["[YearIndexExtra]"] = ommebyearindex 

    elif contestname == "ISL": #ISL
        enunciadostring = ""
        for problem in Plist:
            enunciadostring += GenProbDivISL(problem)
        enunciadosdict = {"[Enunciados]": enunciadostring} 

        dic["[YearIndexExtra]"] = islyearindex

    # Here we replace the GenProbDiv
    index1 = replace_all(indexrawyear, enunciadosdict)

    # Now we can replace again with the correct number of problems
    index2 = replace_all(index1, dic)

    # Write the complete file onto index.html
    indexlink = "ProyectoMURO/public_html/{0}/{1}/index.html".format(str(contestname),str(year))
    with open(indexlink, "w") as f:
        f.write(index2)

    pagecount += 1


    # -------------------------------------------------------------------------------------------------------------
    # Individual problem and solution pages creation

    pnum = 0 

    for problem in Plist:

        pnum += 1 

        dic["[Enunciadoproblema]"] = str(ProblemsList[pnum-1])
        dic["[EnunciadoLatexproblema]"] = str(ProblemsListLatex[pnum-1])
        dic["[nomproblema]"] = problem
        dic["[numproblema]"] = problem
        if contestname == "OMMEB": # Make OMMEB name
            problemname = ""
            for i in problem:
                if i=="n":
                    problemname += "Nivel "
                elif i=="e":
                    problemname += " Equipos "
                elif i=="p":
                    problemname += " Problema "
                else:
                    problemname += i
            dic["[nomproblema]"] = problemname

        problempage = replace_all(problempageraw, dic)

        # Create link to add to file, write
        linkprob = "ProyectoMURO/public_html/{0}/{1}/p{2}.html".format(str(contestname), str(year), problem)

        if contestname in ["OMMEB", "ISL"]: # OMMEB/ISL
            linkprob = "ProyectoMURO/public_html/{0}/{1}/{2}.html".format(str(contestname), str(year), problem)

        with open(linkprob, "w") as f:
            f.write(problempage)

        pagecount += 1

        # Import content
        SolucionProblema = open("./concursos/%s/%s/soluciones/%s.tex" % (contestname, str(year), problem), "r").read()

        if SolucionProblema !="":
            dic["[SolucionProblema]"] = SolucionProblema
        else:
            # If empty add empty format
            dic["[SolucionProblema]"] = emptysoltext

        # Replace all content

        solutionpage = replace_all(solutionpageraw, dic)

        # Create link to add file, write
        linksol = "ProyectoMURO/public_html/{0}/{1}/sol{2}.html".format(str(contestname), str(year), problem)

        with open(linksol, "w") as g:
            g.write(solutionpage)

        pagecount += 1

    return pagecount

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

    pagecount = 0

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
        
        index = replace_all(indexrawcontest, dic) # This is the format, gets replaced with dic

        with open("ProyectoMURO/public_html/%s/index.html" % concurso, "w") as f:
            f.write(index) # Writes the page onto html file

        pagecount += 1

    return pagecount

# ---------------------------------------------------------------------------------------------------------------------
# ReloadOthers 
# Generates pages from info.py file

def ReloadOthers(): 

    pagecount = 0

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

                pagecount += 1
        if i[3] == 1:
            with open("ProyectoMURO/public_html/%s.html" % pagename, "w") as f:
                f.write(pagehtml)

                pagecount += 1

    return pagecount

# ---------------------------------------------------------------------------------------------------------------------
# NoContest
# Generates pages for contests that did not take place

def NoContest(contestname, year, ismin=False, ismax=False):
    nocontestindex = open("generator/formats/no-contest.txt","r").read()
    dic = {
        "[concurso]": str(contestname),
        "[año]": str(year),
        "[añoantes]": r'<a href="./../' + str(year - 1) + r'">◄</a>',
        "[añodespues]": r'<a href="./../' + str(year + 1) + r'">►</a>'
    }

    # This is to remove the arrows for first and last years.
    if ismax:
        dic["[añodespues]"]="" 
    if ismin:
        dic["[añoantes]"]=""

    index = replace_all(nocontestindex, dic)

    indexlink = "ProyectoMURO/public_html/{0}/{1}/index.html".format(str(contestname),str(year))
    with open(indexlink, "w") as f:
        f.write(index)



# ---------------------------------------------------------------------------------------------------------------------
# ReloadPages
# Reloads all the pages in the website. 

def ReloadPages():

    PagesEdited = 0

    # Reload Problem and Solution Pages
    for contest in contestinfo:
        for year in range(contest[1], contest[2]+1):
            if year not in contest[3]: # If the year did take place, generate the page
                # Uses == to check if it is the first or last year.
                PagesEdited += htmlproblems(contest[0], year, year==contest[2], year==contest[1]) 
            else:
                # Add a page: Contest did not take place said year.
                NoContest(contest[0], year, year==contest[2], year==contest[1]) 
                PagesEdited += 1

    # Reload Contest Indexes, including text
    PagesEdited += ReloadContestText()

    # Reload main pages content 
    PagesEdited += ReloadOthers()

    return PagesEdited
