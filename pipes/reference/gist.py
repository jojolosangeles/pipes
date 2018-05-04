#!/usr/bin/python
# from https://www.andreafortuna.org/gist/create-a-github-gist-with-a-simple-python-script/
import os, requests, sys, json


username=sys.argv[2]
password=sys.argv[3]
filename = os.path.basename(sys.argv[1])

content=open(filename, 'r').read()
json_file_message = json.dumps({'files':{filename:{"content":content}}})
print(json_file_message)
r = requests.post('https://api.github.com/gists',json_file_message,auth=requests.auth.HTTPBasicAuth(username, password))
print(r.json()['html_url'])
