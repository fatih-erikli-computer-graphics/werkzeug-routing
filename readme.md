# Werkzeug routing

Simpler implementation of werkzeug-routing.

# Implementation in werkzeug

- https://github.com/pallets/werkzeug/blob/main/src/werkzeug/routing/rules.py#L28

# Example

The function `add_rule` may be called in decorator format as in the example below or a function call by giving the second argument as the function.

    from router import add_rule, resolve

    @add_rule("/")
    def index():
      return "index"

    @add_rule("/words/<word>")
    def word_detail(word):
      return word

    match = resolve("/words/apple")
    if match:
      print(match[1](**match[0]))

# Implementation 