import json
import os
import redis
import requests
from flask import Flask, render_template

app = Flask(__name__)
app.debug = True

je = json.JSONEncoder()

class Backend(object):

    def __init__(self):
        pass

    def tiw_by_id(self, tiw_id):
        return {'id': tiw_id, 'user': 'simon', 'text': 'make a website!', 'done': False}

backend = Backend()

@app.route('/api/id/<tiw_id>')
def api_get_by_id(tiw_id):
  response = backend.tiw_by_id(tiw_id)
  return je.encode(response)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/tiw/<tiw_id>')
def permalink(tiw_id):
  tiw = backend.tiw_by_id(tiw_id)
  return render_template('permalink.html', tiw=tiw)