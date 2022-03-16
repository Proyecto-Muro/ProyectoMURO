#This program copies all problems from IMO Shortlist into a single file.

from processproblem import process_item
from aops_script import get_items

#to get problem i from contest ID X, do
#process_item(get_items(X)[i])
def CollectProblems(ContestCollectionID, ContestName):
    Contest=[ContestName, ContestCollectionID, {}]
    count=0
    items=get_items(Contest[1])
    for i in range(len(items)):
        Contest[2][str(items[i]["item_score"])]=str(items[i]["item_id"])
        count+=1
    #print(Contest)
    ContestStr=''

    for j in Contest[2]:
        ContestProblems=get_items(Contest[2][j])
        ContestStr+="\n%s %s \n\n"%(ContestName, j)
        problemnum=1
        for k in range(len(ContestProblems)):
            Problem=process_item(ContestProblems[k])
            if(Problem !=""):
                ContestStr+="%s %s problem %s:  %s \n"%(ContestName, j, problemnum, Problem)
                #print("%s %s problem %s:  %s \n"%(ContestName, j, problemnum, Problem))
                problemnum+=1
                
    with open(ContestName + ".tex", "w") as f:
        f.write(ContestStr)
