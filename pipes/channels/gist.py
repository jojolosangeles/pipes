import requests, json

class GistOutChannel:
    def __init__(self, filename, username, password):
        print("Creating a GistOutChannel {}, {}, {}".format(filename, username, password))
        self.filename = filename
        self.username = username
        self.password = password
        content = "ho"
        print(json.dumps({'files':{self.filename:{"content":content}}}))

    def send(self, message):
        print(json.dumps({'files':{self.filename:{"content":message}}}))
        r = requests.post('https://api.github.com/gists',json.dumps({'files':{self.filename:{"content":message}}}),auth=requests.auth.HTTPBasicAuth(self.username, self.password))
        print(r.json()['html_url'])