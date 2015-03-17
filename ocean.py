import doctest

import os
import sys
from functools import partial

class Ocean(object):
  def __init__(self, schematic, fname=None, simpath=os.path.abspath(".") + "/simulation"):
    self.schematic = schematic
    self.fname = fname
    self.path = path
    self.simulator = "spectre"

    self.virtuoso_simpath = '/'.join([simpath, self.schematic, self.simulator])

  def __enter__(self):
    if self.fname == None:
      self.f = sys.stdout
    else:
      self.f = open(self.fname, 'w')

    self.simulator("'" + self.simulator)
    self.design(self.virtuoso_simpath + "/netlist/netlist")
    self.resultsDir(self.virtuoso_simpath + "/schematic")
    self.path('/'.join([os.environ['CDK_DIR'], "models", self.simulator, "nom"])

    return self

  def __exit__(self, type, value, traceback):
    self.f.close()

  def put(self, *args):
    self.f.write('(' + '\n  '.join(args) + ')\n')

  def __getattr__(self, name):
    return partial(self.put, name)

if __name__ == '__main__':
  with Ocean() as o:
    o.hello()
