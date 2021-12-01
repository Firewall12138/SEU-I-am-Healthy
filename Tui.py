import requests


def server_post(Subject, Message, Sckey):
    url = 'https://sctapi.ftqq.com/' + Sckey + '.send'
    d = {'title': Subject, 'desp': Message}
    r = requests.post(url, data=d)
