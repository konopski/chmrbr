import requests

GITLAB_URL="http://gitlab/"
API_URL= GITLAB_URL + "api/v3/projects/" 

PRIVATE_TOKEN="mysecret"

project_name = "myproject"
mr_id_from_gui = "1024"
target_branch = "develop"
verbose = True

PRIV_TOKEN_PARAM = { "private_token": PRIVATE_TOKEN }

s = requests.Session()

def gitlab(method, path, params = {}, data = None ):
    req = requests.Request(method=method, url = API_URL + path, params = dict(PRIV_TOKEN_PARAM, **params), data = data )
    r = s.send(req.prepare())
    r.raise_for_status()
    return r.json()

def getProjectId(project_name):
    project = gitlab('GET', "search/" + project_name)
    project_id = project [0] ["id"]
    return project_id

def getOpenMergeRequests(project_id):
    mrs = gitlab('GET', str(project_id) + "/merge_requests/", params = {"state": "opened"})
    return mrs

def findMrByGuiId(mrs, gui_id):
    return [m for m in mrs if str(m["iid"]) == gui_id]

def updateMrTargetBranch(project_id, merge_req_id, target_branch):
    gitlab('PUT', str(project_id) + "/merge_request/" + str(merge_req_id), data = { "target_branch" : target_branch })

project_id = getProjectId(project_name)
open_mrs = getOpenMergeRequests(project_id)
found = findMrByGuiId(open_mrs, mr_id_from_gui)
merge_req = found[0]

if verbose:
    print "Source merge request:"
    print merge_req["id"] 
    print merge_req["source_branch"]
    print merge_req["target_branch"]

updateMrTargetBranch(project_id, merge_req["id"], target_branch)


if verbose:
    try:
        open_mrs = getOpenMergeRequests(project_id)
        found = findMrByGuiId(open_mrs, mr_id_from_gui)
        merge_req = found[0]

        print "\nUpdated merge request:"
        print merge_req["id"] 
        print merge_req["source_branch"]
        print merge_req["target_branch"]

    except:
        pass
