rules = []

def parse_rule(rule):
  r = []
  seek_path_name = False
  buffer = ''
  type = "path"
  for t in rule:
    if t == "<":
      type = "placeholder"
      continue
    if t == ">":
      continue
    if t == "/":
      if seek_path_name:
        r.append([type, buffer])
        if type == "placeholder":
          type = "path"
        buffer = ""
      else:
        seek_path_name = True
      continue
    if seek_path_name:
      buffer += t
  if seek_path_name:
    r.append([type, buffer])
  return r

def add_rule(rule, func=None):
  if func is None:
    def adder(func):
      add_rule(rule, func)
    return adder
  rules.append([parse_rule(rule), func])

def parse_requested_path(path):
  path_requested = []
  buffer = ""
  for t in path:
    if t == "/":
      if buffer:
        path_requested.append(buffer)
      buffer = ""
    else:
      buffer += t
  if buffer:
    path_requested.append(buffer)
  return path_requested

def resolve(path):
  path_requested = parse_requested_path(path)
  for [rule, func] in rules:
    if len(path_requested) == 0:
      if len(rule) == 1 and rule[0][0] == "path" and rule[0][1] == "":
        return [{}, func]
    if len(path_requested) != len(rule):
      continue
    match = False
    skip_until_next = False
    args = []
    for path, [type, name] in zip(path_requested, rule):
      if skip_until_next:
        continue
      if type == "path":
        if path == name:
          match = True
        else:
          match = False
          skip_until_next = True
      else:
        match = True
        args.append([name, path])
    if match:
      return [dict(args), func]
