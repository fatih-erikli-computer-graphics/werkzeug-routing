import json
import http.server
from urllib.parse import unquote_plus
from router import resolve

request = {
  'redirect': None,
  'cookies': {},
  'body': {},
  'query': {},
}

response = {
  'cookies': {},
  'status_code': 200,
  'redirect': None
}

def int_or(d, k, v = None):
  k = d.get(k)
  return int(k) if is_int(k) else v

def is_int(s):
  if isinstance(s, str):
    if s.startswith("-"):
      s = s[1:]
    return s.isdigit()
  else:
    return False

def extend_query_string(path, query, exclude_keys=None):
  query_new = {}
  query_new.update(request["query"])
  query_new.update(query)
  if exclude_keys:
    for k in exclude_keys:
      if k in query_new:
        del query_new[k]
  query_string = make_query_string(query_new)
  if query_string:
    return path + "?" + query_string
  return path

def make_query_string(query):
  return '&'.join(['%s=%s' % (k, v) for (k, v) in query.items()])

def make_cookie_string(cookies):
  return ';'.join(['%s=%s' % (k, v) for (k, v) in cookies.items()])

def parse_cookie_string(cookie_string):
  cookies = {}
  for pair in cookie_string.split(";"):
    key, value = pair.split("=")
    cookies[key.lstrip()] = value
  return cookies

def parse_query_string(query_string):
  query = {}
  for pair in query_string.split("&"):
    key, value = pair.split("=")
    query[key] = value
  return query

def parse_post_body(body):
  buffer = ""
  key = ""
  map = {}
  for t in body:
    if t == "=":
      key = buffer
      buffer = ""
    elif t == "&":
      map[key] = unquote_plus(buffer)
      buffer = ""
      key = ""
    else:
      buffer += t
  map[key] = unquote_plus(buffer)
  return map

class Server(http.server.SimpleHTTPRequestHandler):
  def resolve_view(self, success_status_code):
    if '?' in self.path:
      query_mark_index = self.path.index("?")
      path = self.path[:query_mark_index]
      query_string = self.path[query_mark_index + 1:]
      request["query"] = parse_query_string(query_string)
    else:
      path = self.path
      request["query"] = {}
    cookie_string = self.headers.get("Cookie", "")
    if cookie_string:
      request["cookies"] = parse_cookie_string(cookie_string)
    match = resolve(path)
    if match:
      content = match[1](**match[0])
      if response['redirect'] is None:
        self.send_response(success_status_code)
        write_content = True
      else:
        self.send_response(302)
        self.send_header("Location", response['redirect'])
        self.send_header("Content-Length", "0")
        response['redirect'] = None
        write_content = False
    else:
      write_content = True
      content = "Page not found."
      self.send_response(404)
    http_cookie = make_cookie_string(response["cookies"])
    if http_cookie:
      self.send_header("Set-Cookie", http_cookie)
      response["cookies"] = {}
    if 'content_type' in response:
      self.send_header("Content-Type", response['content_type'])
      del response['content_type']
    else:
      self.send_header("Content-Type", "text/html")
    self.end_headers()
    if write_content:
      if isinstance(content, str):
        self.wfile.write(content.encode())
      else:
        self.wfile.write(content)
    request["cookies"] = {}
    request["body"] = {}

  def do_GET(self):
    request['method'] = "GET"
    self.resolve_view(response["status_code"])

  def not_implemented(self):
    self.send_response(501)
    self.end_headers()
    self.wfile.write("Method is not implemented.".encode())

  def do_POST(self):
    request["method"] = "POST"
    content_type = self.headers.get("Content-Type") or "application/x-www-form-urlencoded"

    try:
      content_length = int(self.headers.get('Content-Length'))
    except (TypeError, ValueError):
      content_length = 0
    data = self.rfile.read(content_length).decode('utf-8')

    if content_type == "application/x-www-form-urlencoded":
      request["body"] = parse_post_body(data)
    elif content_type == "application/json":
      request["body"] = json.loads(data)

    self.resolve_view(201)

  do_PUT = not_implemented
  do_DELETE = not_implemented
  do_PATCH = not_implemented
  do_HEAD = not_implemented
  do_OPTIONS = not_implemented
