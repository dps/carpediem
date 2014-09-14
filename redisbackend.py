import json
import random
import string
import time

ONE_DAY = 24 * 60 * 60
ONE_WEEK = 7 * ONE_DAY

je = json.JSONEncoder()
jd = json.JSONDecoder()

def e(obj):
  return je.encode(obj)

def d(jso):
  if jso:
    return jd.decode(jso)
  else:
    return ''

class RedisBackend(object):

  def __init__(self, redis, instance):
    self._redis = redis
    self._instance = instance

  def _key_user(self, user, key):
  	return self._instance + ':user:' + user['email'] + ':' + key

  def ensure_user(self, user):
    self.maybe_enroll_user(self, user)

  def maybe_enroll_user(self, user):
    if self._redis.exists(self._key_user(user, 'email')):
      return
    self._redis.set(self._key_user(user, 'email'), user['email'])
    self._redis.set(self._key_user(user, 'nickname'), user['nickname'])
    self._redis.set(self._key_user(user, 'avatar_url'), user['picture'])

  def tiw_by_id(self, tiw_id):
    return {'id': tiw_id, 'user': 'simon', 'text': 'make a website!', 'done': False}


