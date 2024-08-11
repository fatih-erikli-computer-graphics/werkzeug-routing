rules = []

def parse_rule(rule):
  r = []
  buffer = ''
  type = "path"
  for t in rule:
    if t == "<":
      if buffer:
        r.append(["path", buffer])
        buffer = ""
      type = "placeholder"
      continue
    if t == ">":
      r.append(["placeholder", buffer])
      buffer = ""
      type = "path"
      continue
    buffer += t
  if buffer:
    r.append([type, buffer])
  return r

def add_rule(rule, func=None):
  if func is None:
    def adder(func):
      add_rule(rule, func)
    return adder
  rules.append([parse_rule(rule), func])

def resolve(path):
  for (rule, func) in rules:
    match = False
    skip_until_next_rule = False
    path_current = path
    args = {}
    for (i, (type, name)) in enumerate(rule):
      if skip_until_next_rule:
        continue
      if type == "path":
        if path_current.startswith(name):
          match = True
          path_current = path_current[len(name):]
          continue
        else:
          match = False
          skip_until_next_rule = True
          continue
      if type == "placeholder":
        next_path = None
        for [_type, _name] in rule[i+1:]:
          if _type == "path":
            next_path = _name
            break
        if next_path:
          if next_path in path_current:
            arg = path_current[:path_current.index(next_path)]
            args[name] = arg
            path_current = path_current[len(arg):]
            match = True
          else:
            skip_until_next_rule = True
            match = False
        else:
          skip_until_next_rule = True
          args[name] = path_current
          path_current = ""
          match = True
    if not path_current and match:
      return args, func
