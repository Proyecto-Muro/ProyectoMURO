import os

# To do list:
# Finish the solution page generator (add to dic)
# Create a generator for ISL pages once it is needed
# Create a generator for OMMEB pages

# ---------------------------------------------------------------------------------------------------------------------
# contestinfo: This list has information on each contest. 
# Format: [contest name (str), first contest year (int), last contest year (int), years omitted (list)]

contestinfo = [
    ["IMO", 1959, 2022, [1980]],       # 0
    ["OMCC", 1999, 2021, []],          # 1
    ["OMM", 1987, 2021, []],           # 2
    ["EGMO", 2012, 2022, []],          # 3
    ["OIM", 1985, 2021, [1986]],       # 4
    ["APMO", 1989, 2022, []],          # 5
    ["RMM", 2008, 2021, []],           # 6
    ["PAGMO", 2021, 2021, []],         # 7
    ["OMMFem", 2021, 2021, []],        # 8
    ["ISL", 1998, 2021, []],           # 9
    ["OMMEB", 2017, 2022 []]           # 10
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
    <div class="alert-secondary alert">\n[Enunciado{0}]\n</div>\n
    <button class="button" onclick=
    "copyEvent(`
    [EnunciadoLatex{0}]
    `)"
    >Copiar LaTeX</button>
    <hr> '''.format(pnum)
    return str(problemdiv)

def GenProbDivISL(problem):
    problemdiv = '''<h3><a href="./{0}.html">{0}</a></h3>\n
    <div class="alert-secondary alert">\n[Enunciado{0}]\n</div>\n
    <button class="button" onclick=
    "copyEvent(`
    [EnunciadoLatex{0}]
    `)"
    >Copiar LaTeX</button>
    <hr> '''.format(problem)
    return str(problemdiv)

def GenProbDivOMMEB(problem):
    problemname = ""
    for i in range(len(problem)):
        if i=="n":
            problemname += "Nivel "
        elif i=="e":
            problemname += " Equipos "
        elif i=="p":
            problemname += " Problema "
        else:
            pronlemname += i
    problemdiv = '''<h3><a href="./{0}.html">{1}</a></h3>\n
    <div class="alert-secondary alert">\n[Enunciado{0}]\n</div>\n
    <button class="button" onclick=
    "copyEvent(`
    [EnunciadoLatex{0}]
    `)"
    >Copiar LaTeX</button>
    <hr> '''.format(problem, problemname)
    return str(problemdiv)

# ---------------------------------------------------------------------------------------------------------------------
# htmlproblems
# This function converts all .tex files in the directory to .html files with the appropriate format.

def htmlproblems(contestname, year, ismax=False, ismin=False):

    # Declare the problems' info, will be set as empty if problem does not exist

    ProblemsList = []
    ProblemsListLatex = []
    ProblemText = ""
    ProblemTextLatex = ""
    ProblemPosition = "1"
    SolProb = ""
    dic = {
        "[Enunciadoproblema]": str(ProblemText),
        "[EnunciadoLatexproblema]": str(ProblemTextLatex),
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
            Plist.append(str(i)[:-4])

    # Contest check

    # Make list of problems: Level 1-3, Problem 1-15, Team 1-8. Example: n3p12, n1e5
    if contestname = "OMMEB":
        Plist = []
        for i in range(1,4):
            for j in range(1, 16):
                Plist.append("n%sp%s"%(i,j))
            for j in range(1, 9):
                Plist.append("n%se%s"%(i,j))

    # Make list of ISL problems
    if contestname = "ISL":
        pass


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
        pstring = yearmod100 + contestname + problem
        if pstring in os.listdir("concursos/asy-imgs"):
            # Add image html to problem 
            # print("Image found:" + pstring)
            imgstr = "\n"+r'<p>' + r'<img src="/images/asy-imgs/{0}.png" alt="{0}.png" height="100" class="center"></p>'.format(pstring)
            EnunciadoProblema += imgstr
            
        # Add entries to dict
        dic[enunciado] = EnunciadoProblema
        dic[enunciadolatex] = EnunciadoLatexProblema

        ProblemsList.append(dic[enunciado]) # Add to ProblemsList for later use
        ProblemsListLatex.append(dic[enunciadolatex])
 
    # -----------------------------------------------------------------------------------------------------------------
    # Year index creation

    # Copy file index.txt as a variable
    indexraw = open("generator/formats/year-index.txt", "r").read()

    # Here we create a dummy dict to add the number of problems, use GenProbDiv
    # This is to account for contests with different number of problems

    if contestname not in ["ISL", "OMMEB"]: # OMMEB/ISL check
        enunciadostring = ""
        for pnum in range(len(Plist)):
            enunciadostring += GenProbDiv(pnum + 1)
        enunciadosdict = {"[Enunciados]": enunciadostring}

    elif contesnmane = "OMMEB": #OMMEB
        enunciadostring = ""
        for problem in Plist:
            enunciadostring += GenProbDivOMMEB(problem)
        enunciadosdict = {"[Enunciados]": enunciadostring}

    elif contestname = "ISL": #ISL
        enunciadostring = ""
        for problem in Plist:
            enunciadostring += GenProbDivISL(problem)
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

    pnum = -1 # This is for OMMEB/ISL

    for problem in Plist:

        try:
            pnum = int(problem)
        except:
            pnum += 1 # OMMEB/ISL

        # Open problem format, replace with problem
        problempageraw = open("generator/formats/problem-page.txt", "r").read()

        dic["[Enunciadoproblema]"] = str(ProblemsList[pnum-1])
        dic["[EnunciadoLatexproblema]"] = str(ProblemsListLatex[pnum-1])
        dic["[numproblema]"] = "problema " + problem
        if contestname = "OMMEB": # Make OMMEB name
            problemname = ""
                for i in range(len(problem)):
                    if i=="n":
                        problemname += "Nivel "
                    elif i=="e":
                        problemname += " Equipos "
                    elif i=="p":
                        problemname += " Problema "
                    else:
                        pronlemname += i
            dic["[numproblema]"] = problemname

        if contestname : "ISL": 
            dic["[numproblema]"] = problem

        problempage = replace_all(problempageraw, dic)

        # Create link to add to file, write
        linkprob = "ProyectoMURO/public_html/{0}/{1}/p{2}.html".format(str(contestname), str(year), problem)

        if contestname in ["OMMEB", "ISL"]: # OMMEB/ISL
            linkprob = "ProyectoMURO/public_html/{0}/{1}/{2}.html".format(str(contestname), str(year), problem)

        with open(linkprob, "w") as f:
            f.write(problempage)

        # Import content
        SolucionProblema = open("./concursos/%s/%s/soluciones/%s.tex" % (contestname, str(year), problem, "r")).read()

        if SolucionProblema !="":
            dic["[SolucionProblema]"] = SolucionProblema
        else:
            # If empty add empty format
            dic["[SolucionProblema]"] = open("generator/texts/emptysol.txt", "r").read()

        # Open format, replace all content
        solutionpageraw = open("generator/formats/solution-page.txt", "r").read()
        solutionpage = replace_all(solutionpageraw, dic)

        # Create link to add file, write
        linksol = "ProyectoMURO/public_html/{0}/{1}/sol{2}.html".format(str(contestname), str(year), problem)

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
# OMMEB Generator
# Creates all OMMEB pages

def ReloadOMMEB():

    ommebinfo = contestinfo[10]

    # Start by making list of all problems in a contest: Level 1-3, Problem 1-15, Team 1-8. Example: n3p12, n1e5
    plist = []
    for i in range(1,4):
        for j in range(1, 16):
            plist.append("n%sp%s"%(i,j))
        for j in range(1, 9):
            plist.append("n%se%s"%(i,j))

    # Make loop for years
    for year in range(ommebinfo[1], ommebinfo[2] + 1):
        if year not in ommebinfo[3]:


    
            # Get each problem info with open() function
            # Paste with format

            # Make year index

    # Generate page index (/OMMEB) and year links

  pass 

# ---------------------------------------------------------------------------------------------------------------------
# ISL Generator
# Creates all ISL pages

def ReloadISL():
    pass

# ---------------------------------------------------------------------------------------------------------------------
# ReloadPages
# Reloads all the pages in the website. 

def ReloadPages():

    # Reload Problem and Solution Pages
    for contest in contestinfo:

        # Reload special contests
        if contest[0] == "OMMEB":
            ReloadOMMEB()
    
        if contest[0] == "ISL":
            ReloadISL()

        else:

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
