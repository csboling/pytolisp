from types import GeneratorType

class Atom(object):
  def __init__(self, x):
    self.name = x
  def __repr__(self):
    return str(self.name)

class Quote(object):
  def __init__(self, x):
    self.contents = x
  def __repr__(self):
    return "'" + lispify(self.contents)

def _parse_args(x):
  return ' '.join(map(lispify, x))

def _parse_sexp(x):
  return '(' + ' '.join(map(lispify, x)) + ')'

def _parse_dict(x):
  return ' '.join(map(_parse_sexp, x.iteritems()))

def _parse_str(x):
  return repr(x).replace("'", '"')

def _parse_other(x):
  try:
    t = x.__name__
    return {
      'Atom'  : repr(x),
      'Quote' : repr(x)
    }.get(t, t)
  except AttributeError:
    return str(x)

def lispify(x):
  '''Convert a Python list into a Lisp-style S-expression.

  >>> lispify([1, 2, [3, (str, repr), "4"], Atom("cat"), Quote([5, "dog"])])
  '(1 2 (3 (str repr) "4") cat \\'(5 "dog"))'
  '''
  return {
    list          : _parse_sexp,
    tuple         : _parse_sexp,
    dict          : _parse_dict,
    GeneratorType : _parse_args,
    str           : _parse_str
  }.get(type(x), _parse_other)(x)

if __name__ == '__main__':
  import doctest
  doctest.testmod()
