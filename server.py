import http.server
from router import resolve

class Server(http.server.SimpleHTTPRequestHandler):
  def do_GET(self):
    match = resolve(self.path)
    content = ""
    if match:
      content = match[1](**match[0])
      self.send_response(200)
    else:
      content = "Page not found."
      self.send_response(404)
    self.end_headers()
    self.wfile.write(content.encode())

  def not_implemented(self):
    self.send_response(501)
    self.end_headers()
    self.wfile.write("Method is not implemented.".encode())

  do_POST = not_implemented
  do_PUT = not_implemented
  do_DELETE = not_implemented
