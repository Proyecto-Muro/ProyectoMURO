import os

def replace_all(text, dic): 
    for i, j in dic.items():
        text = str(text).replace(str(i), str(j))
    return text

replacedict = {
	"<br>": r" \newline ",
	"<ul>": r" \begin{itemize} ",
	"</ul>": r" \end{itemize} ",
	"<ol>": r" \begin{enumerate} ",
	"</ol>": r" \end{enumerate} ",
	"<li>": r" \item ",
	"</li>": "",
	"<i>": r"\emph{",
	"</i>": r"}"
}

def htmltotex(text):
	return replace_all(text,replacedict)

counter=0
contestlist = ["APMO", "EGMO", "IMO", "ISL", "OIM", "OMCC", "OMM", "RMM", "PAGMO", "OMMFem", "OMMEB"]
for i in contestlist:
	for j in os.listdir("concursos/"+i):
		if j[0]!=".":
			for k in os.listdir("concursos/%s/%s/enunciados"%(i,j)):
				if k[0]!=".":
					fhtml = open("concursos/%s/%s/enunciados/%s"%(i,j,k), "r").read()
					if fhtml!="":
						counter+=1
					ftex = htmltotex(fhtml)
					testempty = open("concursostex/%s/%s/enunciados/%s"%(i,j,k), "r").read()
					if testempty =="":
						with open("concursostex/%s/%s/enunciados/%s"%(i,j,k), "w") as file:
							file.write(ftex)

print("Problems in database: " + str(counter))