import doctest

import os
import sys
from functools import partial

from lispify import lispify, Atom, Quote

def path(*args):
  return os.path.abspath(os.path.join(*args))

class OceanManager(object):
  def __init__(self, schematic, path, simpath, modelfile):
    self.schematic = schematic
    self.path = path
    self.simulator = "spectre"
    self.abs_simpath = os.path.join(simpath, 
                                    self.schematic, 
                                    self.simulator)
    self.modelfiles = [(os.path.abspath(x), "") for x in 
                        [os.environ['CDK_DIR'] + "MSU/allModels.scs",
                         os.path.join(self.path, modelfile)]]

class Ocean(object):
  def __init__(self, fname, *args, **kwargs):
    self.fname = fname
    self.mgr = OceanManager(*args, **kwargs)

  def __exit__(self, type, value, traceback):
    self.f.close()

  def __enter__(self):
    if self.fname == None:
      self.f = sys.stdout
    else:
      self.f = open(self.fname, 'w')

    self.simulator(Quote(self.mgr.simulator))
    # self.simulator(self._quote(self.mgr.simulator))
    self.design(
      path(
        self.mgr.abs_simpath, 
        "netlist/netlist"))
    self.resultsDir(
      path(
        self.mgr.abs_simpath, 
        "schematic"))
    self.path(
      path(
        os.environ['CDK_DIR'], 
        "models", 
        self.mgr.simulator, 
        "nom"))
    self.modelFile(
      map(Quote, self.mgr.modelfiles))
    # self.modelFile(
    #   *(self._quote(
    #      self._list(
    #        map(self._string, x))) 
    #    for x in self.mgr.modelfiles))

    return self

  def _put(self, *args):
    self.f.write(lispify(args) + '\n')
#    self.f.write(self._list(args, sep='\n  ') + '\n')

  def __getattr__(self, name):
    return partial(self._put, Atom(name))

if __name__ == '__main__':
  with Ocean() as o:
    o.hello()
