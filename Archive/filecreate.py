import os

islproblems = [ 
    [5,7,8,8], # 1998
    [6,7,8,6],
    [7,6,8,6],
    [6,8,8,6],
    [6,7,8,6],
    [6,6,7,8],
    [7,8,8,7],
    [5,8,7,7],
    [6,7,10,7],
    [7,8,8,7],
    [7,6,7,6],
    [7,8,8,7],
    [8,7,7,6],
    [7,7,8,8],
    [7,7,8,8],
    [6,8,6,7],
    [6,9,7,8],
    [6,7,8,8],
    [8,8,8,8],
    [8,8,8,8],
    [7,7,7,7],
    [7,9,8,8],
    [8,8,9,7],
    [8,8,8,8] # 2021
]

for year in range(1998,2022):
    Plist = []
    letters = ["A", "C", "G", "N"]
    areas = islproblems[year - 1998]
    for i in range(4): 
        for j in range(areas[i]):
            Plist.append(letters[i]+str(j+1))

    newpath = "ISL/%s"%(year)
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    for k in Plist:
        if not os.path.exists("ISL/%s/enunciados/%s.html"%(year, k)):
            fp=open("ISL/%s/%s.html"%(year, k),"w")
            htext=""
            fp.write(htext)
            fp.close
        if not os.path.exists("ISL/%s/sol%s.html"%(j, k)):
            fp=open("ISL/%s/sol%s.html"%(year, k),"w")
            htext=""
            fp.write(htext)
            fp.close


    fp=open("ISL/%s/index.html"%(year),"w")
    htext=""
    fp.write(htext)
    fp.close
