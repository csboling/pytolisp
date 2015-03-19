'''
A shallow embedding to compile a subset of Python to Lisp.
'''

import argparse
import sys

import inspect
import ast
import meta
import lispify as lpfy

def compose(*args):
  return reduce(lambda f, g: lambda x: f(g(x)), args)

class ToLisp(ast.NodeVisitor):
  def __init__(self, outf, *args, **kwargs):
    ast.NodeVisitor.__init__(self, *args, **kwargs)
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

def example():
  y * 2
  [y] * 2
  str('3')

def parse_func(outf, func):
  t = ast.parse(inspect.getsource(func))
  ToLisp(outf).visit(t)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('fname', type=argparse.FileType('w'), 
                      nargs='?', default=sys.stdout)
  args = parser.parse_args()

  parse_func(args.fname, example)
