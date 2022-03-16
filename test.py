import os

#print(open("generator/yearindex.txt", "r").read())

#Plist=os.listdir("./concursos/OMM/1987/enunciados")
#Plist.sort()
#for i in Plist:
#    print(i[:-4])

def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(str(i), str(j))
    return(text)

contestname="OMM"
year="1987"
#Plist=os.listdir("./concursos/%s/%s/enunciados"%(contestname,year))
#Plist.sort()
#for i in Plist:
#    print(i[:-4])
ProblemsList=[]
Problem=""
ProblemPosition="1"
dic = {
    "[Enunciadoproblema]": str(Problem),
    "[concurso]": str(contestname),
    "[año]": str(year),
    "[numproblema]": str(ProblemPosition)
    }
pcount=0
Plist=os.listdir("./concursos/%s/%s/enunciados"%(contestname,year))
Plist.sort()
for i in Plist:
    enunciado="[Enunciado"+str(i[:-4])+"]"
    dic[enunciado]=open("./concursos/%s/%s/enunciados/%s.tex"%(contestname,year,i[:-4])).read()
    ProblemsList.append(dic[enunciado])


#YEAR FILE CREATION
#copy file index.txt as a variable
indexraw=open("generator/yearindex.txt", "r").read()
#replace variables
index=replace_all(indexraw, dic)
#write onto index.html
with open("ProyectoMURO/public_html/" + str(contestname)+"/"+str(year)+"/"+"index.html", "w") as f:
   f.write(index)


    
