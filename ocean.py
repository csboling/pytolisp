import doctest

import os
import sys
from functools import partial

from lispify import lispify, Atom, Quote

def path(*args):
  return os.path.abspath(os.path.join(*args))

class OceanManager(object):
  def __init__(self, schematic, virtuosopath, simpath, modelfile):
    self.schematic = schematic
    self.path = virtuosopath
    self.simulator = "spectre"
    try:
      self.CDK_DIR = os.environ['CDK_DIR']
    except KeyError:
      self.CDK_DIR = '.'
    self.abs_simpath = os.path.join(simpath, 
                                    self.schematic, 
                                    self.simulator)
    self.modelfiles = [(path(x), "")
                       for x in [self.CDK_DIR + "MSU/allModels.scs",
                                 path(self.path, modelfile)]]

class Ocean(object):
  def __init__(self, fname, *args, **kwargs):
    self.fname = fname
    self.mgr = OceanManager(*args, **kwargs)

  def __call__(self, *args):
    self.f.write(lispify(args) + '\n')    

  def __enter__(self):
    if self.fname == None:
      self.f = sys.stdout
    else:
      self.f = open(self.fname, 'w')
    self._setup()
    return self

  def __exit__(self, type, value, traceback):
    self.f.close()

  def _setup(o):
    o(Atom("simulator"), 
        Quote(Atom(o.mgr.simulator)))
    o(Atom("design"), 
        path(o.mgr.abs_simpath, "netlist/netlist"))
    o(Atom("resultsDir"),
        path(o.mgr.abs_simpath, 
             "models", 
             o.mgr.simulator,
             "nom"))
    o(Atom("modelFile"),
        map(Quote, o.mgr.modelfiles))

if __name__ == '__main__':
  with Ocean() as o:
    pass
