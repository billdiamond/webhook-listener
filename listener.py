"""Listener module."""
from sys import platform as _platform
from os import environ

from pync import Notifier
from flask import Flask, request
app = Flask(__name__)

# check for ngrok subdomain
ngrok = environ.get("NGROK_SUBDOMAIN", "")

def displayIntro():
    if ngrok:
        print 'You can access this webhook publicly via at http://%s.ngrok.io/webhook\
        You can access ngrok\'s web interface via http://localhost:4040' % ngrok
    else:
        print 'Webhook server online! Go to http://localhost:5000'

def displayHTML(request):
    if ngrok:
        return 'Webhook server online! Go to <a href="https://bitbucket.com">Bitbucket</a> to configure your repository webhook for <a href="http://%s.ngrok.io/webhook">http://%s.ngrok.io/webhook</a> <br />\
            You can access ngrok\'s web interface via <a href="http://localhost:4040">http://localhost:4040</a>' % (ngrok,ngrok)
    else:
        return 'Webhook server online! Go to <a href="https://bitbucket.com">Bitbucket</a> to configure your repository webhook for <a href="%s/webhook">%s/webhook</a>' % (request.url_root,request.url_root)

@app.route('/', methods=['GET'])
def index():  
    return displayHTML(request)

@app.route('/webhook', methods=['GET', 'POST'])
def tracking():  
    if request.method == 'POST':
        data = request.get_json()
        commit_author = data['actor']['username']
        commit_hash = data['push']['changes'][0]['new']['target']['hash'][:7]
        commit_url = data['push']['changes'][0]['new']['target']['links']['html']['href']
        # Show notification if operating system is OS X
        if _platform == "darwin":
            from pync import Notifier
            Notifier.notify('%s committed %s\nClick to view in Bitbucket' % (commit_author, commit_hash), title='Webhook received!', open=commit_url)
        else:
            print 'Webhook received! %s committed %s' % (commit_author, commit_hash)
        return 'OK'
    else:
        return displayHTML(request)

if __name__ == '__main__':
    displayIntro()
    app.run(host='0.0.0.0', port=5000, debug=True)