import requests, json

class GistOutChannel:
    def __init__(self, gist_id_channel, filename, username, password):
        self.gist_id_channel = gist_id_channel
        self.filename = filename
        self.username = username
        self.password = password

    def send(self, message):
        r = requests.post('https://api.github.com/gists',json.dumps({'files':{self.filename:{"content":message}}}),auth=requests.auth.HTTPBasicAuth(self.username, self.password))
        self.gist_id_channel.send(r.json()['html_url'])