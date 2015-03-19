'''
A shallow embedding to compile a subset of Python to Lisp.
'''

import argparse
import sys
from StringIO import StringIO

import inspect
import ast
import meta
import lispify as lpfy

def compose(*args):
  return reduce(lambda f, g: lambda x: f(g(x)), args)

class Embedding(object):
  '''
  This only operates on ast.Expr, so assignments, return
  expressions, etc. should be excluded. Therefore you
  basically write a 'script' by not assigning any names,
  and
  '''
  def __init__(self, outf=None):
    if outf == None:
      outf = StringIO()
    self.outf = outf

  @staticmethod
  def toSource(x):
    return meta.dump_python_source(x).strip()

  @classmethod
  def toList(cls, x):
    if isinstance(x, ast.Name):
      return lpfy.Atom(x.id)
    # Python-style function calls are evaluated
    elif isinstance(x, ast.Call):
      return lpfy.Atom(eval(cls.toSource(x)))
    elif isinstance(x, ast.Num):
      return x.n
    elif isinstance(x, ast.Str):
      return lpfy._parse_str(x.s)
    elif isinstance(x, ast.List):
      return map(cls.toList, x.elts)
    elif isinstance(x, ast.UnaryOp):
      return [lpfy.Atom(cls.toSource(x.op)),
                cls.toList(x.operand)]
    elif isinstance(x, ast.BinOp):
      return [lpfy.Atom(cls.toSource(x.op)),
                cls.toList(x.left),
                cls.toList(x.right)]
    else:
     return cls.toSource(x)

  def visit_Expr(self, node):
    parsed = self.toList(node.value)
    self.outf.write(lpfy.lispify(parsed) + '\n')
    return ast.Expr() # replace with an empty node

def parse_ast(t, outf=None):
  embedding = Embedding(outf)
  for __x in t:
    if isinstance(__x, ast.Expr):
      embedding.visit_Expr(__x)
    else:
      exec(meta.dump_python_source(__x))

  try:
    return embedding.outf.getvalue()
  except AttributeError:
    return None

def parse_func(func, outf=None):
  source = inspect.getsource(func)
  func_ast = ast.parse(source).body[0]
  return parse_ast(func_ast.body, outf=outf)

def parse(source, outf=None):
  return parse_ast(ast.parse(source), outf=outf)

def example():
  y * 2
  x = 7*'\x30'
  print x
  [y] * 2
  str('3')

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('outfname', type=argparse.FileType('w'), 
                      nargs='?', default=sys.stdout)
  args = parser.parse_args()

  parse_func(example, outf=args.outfname)
