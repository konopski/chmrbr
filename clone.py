import requests
import argparse 
import functools

execfile('config.py')

API_URL= GITLAB_URL + "api/v3/projects/" 

PRIV_TOKEN_PARAM = { "private_token": PRIVATE_TOKEN }

s = requests.Session()

def gitlab(method, path, params = {}, data = None ):
    req = requests.Request(method=method, url = API_URL + path, params = dict(PRIV_TOKEN_PARAM, **params), data = data )
    r = s.send(req.prepare())
    r.raise_for_status()
    return r.json()

project = gitlab('GET', "", {'simple': 'true', 'per_page': '100'} )

def ssl_url(jsonobj):
    return jsonobj[u'ssh_url_to_repo']

for x in list(map(ssl_url, project)): 
    print "git clone " + x
 
