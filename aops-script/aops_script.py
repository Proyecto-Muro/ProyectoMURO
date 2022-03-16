import datetime
import json
import re
import requests
import sqlite3
import subprocess
"""
import create_sql
"""



global aopssid, aops_session_id
aopssid = ""
aops_session_id = ""




def renew_aops_session(aops_id):
    global aopssid, aops_session_id
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get("https://artofproblemsolving.com/", headers=headers)
    try:
        aopssid = re.search(r"aopssid=([^;]*);", response.headers["set-cookie"]).group(1)
        aops_session_id = re.search(r"AoPS\.session = {\"id\":\"([^\"]*)\"", response.content.decode("utf-8")).group(1)
    except:
        print("Error while curling `{aops_id}`.".format(aops_id=aops_id))
        aopssid = input("New aopssid: ")
        aops_session_id = input("New aops_session_id: ")


def aops(url, aops_id):
    global aopssid, aops_session_id
    response = url.format(aopssid=aopssid, aops_id=aops_id, aops_session_id=aops_session_id)
    response = subprocess.run(response, shell=True, capture_output=True)
    if response.returncode != 0:
        renew_aops_session(aops_id)
        return(aops(url, aops_id))
    response = json.loads(response.stdout.decode("utf-8"))
    try:
        if type(response["response"]) == str:
            raise Exception("INVALID SESSION")
        return(response["response"])
    except:
        renew_aops_session(aops_id)
        return(aops(url, aops_id))


def get_items(aops_id):
    return(aops("curl 'https://artofproblemsolving.com/m/community/ajax.php' -H 'Cookie: aopsuid=1; aopssid={aopssid}' " \
        + "--data-raw 'category_id={aops_id}&a=fetch_more_items&fetch_all=1&aops_session_id={aops_session_id}' --silent", aops_id)["items"])


def get_data(aops_id):
    return(aops("curl 'https://artofproblemsolving.com/m/community/ajax.php' -H 'Cookie: aopsuid=1; aopssid={aopssid}' "
        + "--data-raw 'category_id={aops_id}&a=fetch_category_data&aops_session_id={aops_session_id}' --silent", aops_id)["category"])



# Scan a string for a year
def get_year_from_string(string):
    for i in re.findall(r"\d\d\d\d", string):
        try:
            if 1900 < int(i) < 2100:
                return(str(int(i)))
        except:
            pass
    return(None)


# Checks if category_name or short_description contains the year
def get_year(category):
    try:
        output = get_year_from_string(category["category_name"])
        if output: return(output)
    except: pass
    try:
        output = get_year_from_string(category["short_description"])
        if output: return(output)
    except: pass
    return(None)




def process_contest(aops_id, indent=0, path="", quick=False):
    if quick:
        with open("problems/quick_processed_ids.txt") as f:
            if path + str(aops_id) + "\n" in f.readlines():
                return
    with open("problems/processed_ids.txt") as f:
        if path + str(aops_id) + "\n" in f.readlines():
            return
    data = get_data(aops_id)
    items = get_items(aops_id)

    year = get_year(data)
    if year:
        if not(-3 < (int(year) - datetime.datetime.now().year)):
            with open("problems/processed_ids.txt", "a") as f:
                f.write(path + str(aops_id) + "\n")

    subprocess.run("mkdir -p problems/" + path + str(aops_id) + "/", shell=True)
    with open("problems/" + path + str(aops_id) + "/data.json", "w") as f:
        f.write(json.dumps(data))
    with open("problems/" + path + str(aops_id) + "/items.json", "w") as f:
        f.write(json.dumps(items))


def scan_folder(aops_id, indent=0, path="", quick=False):
    if quick:
        with open("problems/quick_processed_ids.txt") as f:
            if path + str(aops_id) + "\n" in f.readlines():
                return
    with open("problems/processed_ids.txt") as f:
        if path + str(aops_id) + "\n" in f.readlines():
            return
    data = get_data(aops_id)
    items = get_items(aops_id)
    print(" "*indent + data["category_name"])

    for i in items:
        if i["item_type"] == "folder":
            scan_folder(i["item_id"], indent+1, path + str(aops_id) + "/")
        elif i["item_type"] == "view_posts":
            process_contest(i["item_id"], indent+1, path + str(aops_id) + "/")
        else:
            print(aops_id, i["item_type"])

    year = get_year(data)
    if year:
        if not(-3 < (int(year) - datetime.datetime.now().year)):
            with open("problems/processed_ids.txt", "a") as f:
                f.write(path + str(aops_id) + "\n")

    subprocess.run("mkdir -p problems/" + path + str(aops_id) + "/", shell=True)
    with open("problems/" + path + str(aops_id) + "/data.json", "w") as f:
        f.write(json.dumps(data))
    with open("problems/" + path + str(aops_id) + "/items.json", "w") as f:
        f.write(json.dumps(items))
