import argparse
import os

import ocean

def main(script_name, schematic,
         path=os.path.abspath("."), simpath=None):
  if simpath == None:
    simpath = os.path.join(path, 'simulation')
  with ocean.Ocean(fname=script_name, schematic=schematic, 
                   path=path, simpath=simpath) as oc:
    pass

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
             description=
             '''
             Automated parametric analysis for some simulations with Cadence Virtuoso.
             '''
           )
  parser.add_argument('schematic', type=str,
                      help='Name of schematic cellview')
  parser.add_argument('script_name', type=file, 
                      nargs='?', default=None,
                      help='Name of Ocean script to generate')
  parser.add_argument('--path', dest='path', type=str, 
                      nargs='?', default='../virtuoso',
                      help='Path to virtuoso files, if not ../virtuoso')
  parser.add_argument('--simpath', dest='simpath', 
                      type=str, default=None,
                      help='Directory in which to run the simulator, if not <path>/simulation')
  args = parser.parse_args()

  main(schematic=args.schematic, 
       script_name=args.script_name, 
       path=args.path, simpath=args.simpath)
