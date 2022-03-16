import os

a=[
    #["IMO",1959,6],
   #["ISL",1959,30],
   #["OMCC",1999,6],
   # ["OMM",1987,6],
  # ["EGMO",2012,6],
  # ["OIM",1985,6],
  # ["RMM",2008,6],
  #  ["APMO",1989,5]
  ["OMCC", 1999, 6]

   ]

for i in a:
    for j in range(i[1],2022):
        newpath = "%s/%s/soluciones"%(i[0], j)
        if not os.path.exists(newpath):
            os.makedirs(newpath)        
        for k in range(1,(i[2]+1)):
            if not os.path.exists("%s/%s/enunciados/%s.tex"%(i[0], j, k)):
                fp=open("%s/%s/enunciados/%s.tex"%(i[0], j, k),"w")
                htext=""
                fp.write(htext)
                fp.close
            if not os.path.exists("%s/%s/soluciones/%s.tex"%(i[0], j, k)):
                fp=open("%s/%s/soluciones/%s.tex"%(i[0], j, k),"w")
                htext=""
                fp.write(htext)
                fp.close

'''
i=["ISL",1959,30]

for j in range(1993,2022):
    newpath = "%s/%s/enunciados"%(i[0], j)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    newpath = "%s/%s/soluciones"%(i[0], j)
    if not os.path.exists(newpath):
        os.makedirs(newpath)        
    for k in range(1,9):
        for n in ["A","C","G","N"]:
            fp=open("%s/%s/enunciados/%s%s.tex"%(i[0], j, n, k),"w")
            htext=""
            fp.write(htext)
            fp.close
            fp=open("%s/%s/soluciones/%s%s.tex"%(i[0], j, n, k),"w")
            htext=""
            fp.write(htext)
            fp.close


'''
