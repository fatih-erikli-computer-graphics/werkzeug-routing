import socketserver
from server import Server

from router import add_rule

PORT = 4000

@add_rule("/")
def index():
  return "index"

@add_rule("/words/<word>")
def word_detail(word):
  return word

with socketserver.TCPServer(("0.0.0.0", PORT), Server) as httpd:
  print("serving at port", PORT)
  httpd.serve_forever()
