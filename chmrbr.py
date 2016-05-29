import requests
import argparse 

execfile('config.py')

API_URL= GITLAB_URL + "api/v3/projects/" 

PRIV_TOKEN_PARAM = { "private_token": PRIVATE_TOKEN }

parser = argparse.ArgumentParser() 
parser.add_argument("-p", "--project_name", dest="project_name", help="gitlab project name", type=str, required=True)
parser.add_argument("-id", "--id", dest="mr_id", help="MR id visible in gitlab", type=int, required=True)
parser.add_argument("-t", "--target_branch", dest="target_branch", help="new target branch", type=str, required=True)
parser.add_argument("-v", "--verbose", dest="verbose", help="display information", type=bool, required=False, default=False)
args = parser.parse_args()
project_name = args.project_name
mr_id_from_gui = str(args.mr_id)
target_branch = args.target_branch
verbose = args.verbose

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
