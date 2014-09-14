import json
import os
import redis
import requests
from flask import Flask, request, jsonify, session, redirect, render_template, send_from_directory
from redisbackend import RedisBackend

app = Flask(__name__)
app.debug = True
app.secret_key = os.environ["FLASK_SECRET_KEY"]

je = json.JSONEncoder()

appredis = redis.StrictRedis(
    host=os.environ['REDIS_HOST'], 
    port=9148,
    db=0,
    password=os.environ['REDIS_KEY'])

backend = RedisBackend(appredis, 'carpe_test')

@app.route('/callback')
def callback_handling():
  env = os.environ
  code = request.args.get('code')

  json_header = {'content-type': 'application/json'}

  token_url = "https://{domain}/oauth/token".format(domain=env["AUTH0_DOMAIN"])
  token_payload = {
    'client_id' : env['AUTH0_CLIENT_ID'], \
    'client_secret' : env['AUTH0_CLIENT_SECRET'], \
    'redirect_uri' : env['AUTH0_CALLBACK_URL'], \
    'code' : code, \
    'grant_type': 'authorization_code' \
  }

  token_info = requests.post(token_url, data=json.dumps(token_payload), headers = json_header).json()

  user_url = "https://{domain}/userinfo?access_token={access_token}"  \
    .format(domain=env["AUTH0_DOMAIN"], access_token=token_info['access_token'])

  user_info = requests.get(user_url).json()

  # We're saving all user information into the session
  session['profile'] = user_info

  # Redirect to the User logged in page that you want here
  return redirect('/')

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if not session.has_key('profile'):
      # Redirect to Login page here
      return redirect('/')
    backend.ensure_user(session['profile'])
    return f(*args, **kwargs)

  return decorated

# The app itself...  
@app.route('/api/id/<tiw_id>')
def api_get_by_id(tiw_id):
  response = backend.tiw_by_id(tiw_id)
  return je.encode(response)

@app.route('/')
def index():
  user = None
  if session.has_key('profile'):
    user = session['profile']
  backend.ensure_user(user)
  return render_template('index.html', user=user)

@app.route('/tiw/<tiw_id>')
def permalink(tiw_id):
  user = None
  if session.has_key('profile'):
    user = session['profile']
  tiw = backend.tiw_by_id(tiw_id)
  return render_template('permalink.html', tiw=tiw, user=user)