#ok so this somehow works.

def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(str(i), str(j))
    return(text)




def htmlproblems(contestname, year, numproblems):
    #define the problems, set as empty if problem does not exist
    dic = {
        "[Enunciado1]": P1,
        "[Enunciado2]": P2,
        "[Enunciado3]": P3,
        "[Enunciado4]": P4,
        "[Enunciado5]": P5,
        "[Enunciado6]": P6,
        "[Enunciadoproblema]": Problem,
        "[concurso]": contestname,
        "[año]": year,
        "[numproblema]": ProblemPosition
        }
    ProblemsList=[P1,P2,P3,P4,P5,P6]
    #
    #copy file index.txt as a variable
    indexraw=open("index.txt", "r").read()
    #replace variables
    index=replace_all(indexraw, dic)
    #write onto index.html
    with open(str(contestname)+"/"+str(year)+"/"+"index.html", "w") as f:
       f.write(index)
    
    
    for i in range(numproblems):
        #create file pi.html, replace
        problempageraw=open("problem.txt", "r").read()
        #replace variables
        #define Problem and ProblemPosition in dic
        Problem=ProblemsList[i]
        ProblemPosition=i+1
        problempage=replace_all(problempageraw, dic)
        with open(str(contestname)+"/"+str(year)+"/"+"p"+str(ProblemPosition)+".html", "w") as f:
            f.write(problempage)
        #create file soli.html













