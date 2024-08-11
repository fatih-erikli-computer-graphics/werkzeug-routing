from router import resolve, add_rule

add_rule("/", lambda: "home")
add_rule("/register", lambda: "register")
add_rule("/register/<referrer>", lambda referrer: "register referrer" + referrer)
add_rule("/<icon_set>/<name>.png", lambda icon_set, name: "icon:" + icon_set + name)
add_rule("/<user>/pic/<picid>", lambda user, picid: "userpic:" + user + picid)
add_rule("/<user>", lambda user: "user:" + user)

def route(path):
  match = resolve(path)
  return match[1](**match[0])

assert route("/") == "home"
assert route("/register") == "register"
assert route("/register/kartonpr") == "register referrerkartonpr"
assert route("/solitaire/diamond.png") == "icon:solitairediamond"
assert route("/ramm") == "user:ramm"
assert route("/ramm/pic/2") == "userpic:ramm2"
