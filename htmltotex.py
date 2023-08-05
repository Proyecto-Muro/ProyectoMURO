# Changes problems from HTML to TeX and saves in corresponding directory
# Also counts # of problems and saves them in .json file for further use

import os
import json

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

probdict = {}

counter=0
contestlist = ["APMO", "EGMO", "IMO", "ISL", "OIM", "OMCC", "OMM", "RMM", "PAGMO", "OMMFem", "OMMEB", "MXTST"]
for contest in contestlist:
	for year in os.listdir("concursos/"+contest):
		if year[0]!=".":
			for problem in os.listdir("concursos/%s/%s/enunciados"%(contest,year)): # problem is a .tex file
				if problem[0]!=".":
					fhtml = open("concursos/%s/%s/enunciados/%s"%(contest,year,problem), "r").read()
					if fhtml!="":

						# Add counter
						counter += 1 

						# Create PUID
						puid = str(int(year) % 100) + contest + problem[:-4]

						# Convert html to tex
						ftex = htmltotex(fhtml)

						# Add to dict
						probdict[puid] = ftex
						
						testempty = open("concursostex/%s/%s/enunciados/%s"%(contest,year,problem), "r").read()
						if testempty =="":
							with open("concursostex/%s/%s/enunciados/%s"%(contest,year,problem), "w") as file:
								file.write(ftex)



print("Problems in database: " + str(counter))

# Save to JSON

with open('concursos/problemas.json', 'w') as f:
    json.dump(probdict, f, ensure_ascii=False, indent=4)

os.system('cp concursos/problemas.json ProyectoMURO/public_html/scripts/problemas.js')


