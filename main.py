import json
import os
import socketserver
from urllib.parse import unquote_plus
from server import Server

from router import add_rule

PORT = 4001

@add_rule("/set/<key>/<value>")
def index(key, value):
  f = open(os.path.join(os.path.dirname(__file__), "data", key), "w")
  f.write(unquote_plus(value))
  f.close()
  return json.dumps({
    "result": "ok"
  })

@add_rule("/del/<key>")
def delete(key):
  path = os.path.join(os.path.dirname(__file__), "data", key)
  exists = os.path.exists(path)
  if exists:
    result = True
    os.remove(path)
  else:
    result = False
  return json.dumps({
    "result": result
  })

@add_rule("/get/<key>")
def index(key):
  exists = os.path.exists(os.path.join(os.path.dirname(__file__), "data", key))
  if exists:
    f = open(os.path.join(os.path.dirname(__file__), "data", key))
    result = f.read()
    f.close()
  else:
    result = None
  return json.dumps({
    "result": result
  })

@add_rule("/exists/<key>")
def index(key):
  exists = os.path.exists(os.path.join(os.path.dirname(__file__), "data", key))
  return json.dumps({
    "result": 1 if exists else 0
  })

with socketserver.TCPServer(("0.0.0.0", PORT), Server) as httpd:
  print("serving at port", PORT)
  httpd.serve_forever()
