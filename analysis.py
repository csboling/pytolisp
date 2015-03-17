import argparse
import os

import ocean

def main(fname, path=os.path.abspath("."), simpath=None):
  if simpath == None:
    simpath = path + '/simulation'
  with ocean.Ocean(fname=fname, simpath=simpath) as oc:
    pass

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
             description=
             '''
             Automated parametric analysis for some simulations with Cadence Virtuoso.
             '''
           )
  parser.add_argument('fname', dest=fname, type=file, default=None,
                      help='Name of Ocean script to generate')
  parser.add_argument('path', dest=path, type=str, default='./virtuoso',
                      help='Path to virtuoso files, if not ./virtuoso')
  parser.add_argument('--simpath', dest=simpath, type=str, default=None,
                      help='Directory in which to run the simulator, if not ./simulation')
  args = parser.parse_args()

  main(args.fname, path=args.path, simpath=args.simpath)
