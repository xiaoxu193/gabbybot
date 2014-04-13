"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask
from flask import request
import sys
sys.path.insert(0, 'lib/pyaiml')
import aiml
import os.path

k = aiml.Kernel()
if os.path.isfile("lib/pyaiml/standard.brn"):
    k.bootstrap(brainFile = "lib/pyaiml/standard.brn")
else:
    k.bootstrap(learnFiles = "lib/pyaiml/std-startup.xml", commands = "load aiml b")
    k.saveBrain("lib/pyaiml/standard.brn")

app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/', methods=['POST'])
def bus():
    """Return a friendly HTTP greeting."""
    if request.method == 'POST':
    	number = request.form['From']
    	body = request.form['Body']
    	response = k.respond(body, number)
    	return "<?xml version='1.0' encoding='UTF-8'?><Response><Message>" + response + "</Message></Response>"


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def page_not_found(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
