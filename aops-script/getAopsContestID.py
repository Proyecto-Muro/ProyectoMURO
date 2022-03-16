#Script for getting aops IDs from get_items(collection_id)

from aops_script import get_items

def ContestYearIDs(contest_id):
    count=0
    items=get_items(contest_id)
    for i in items:
        #print(str(items[count]["item_id"]))
        print(str(items[count]["item_score"]) + ": " + str(items[count]["item_id"]))
        count +=1
