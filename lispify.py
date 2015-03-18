def parse_list(x):
  if x == []:
    return '()'
  return '(' + ' '.join(map(parse, x)) + ')'

def parse_str(x):
  if x == '':
    return ''
  elif x[0] == "'":
    return "'" + x[1:]
  return repr(x).replace("'", '"')

def parse_other(x):
  try:
    return x.__name__
  except AttributeError:
    return str(x)

def parse(x):
  return {
    list : parse_list,
    str  : parse_str
  }.get(type(x), parse_other)(x)
