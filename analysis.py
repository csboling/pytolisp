import argparse
import os

import ocean
import lispify

def main(script_name, schematic,
         path=os.path.abspath("."), simpath=None,
         *args, **kwargs):
  if simpath == None:
    simpath = os.path.join(path, 'simulation')

  designVars = {
    "Beta"   : "2",
    "f_CLK"  : "100M",
    "Nsize"  : "1",
    "t_FALL" : "100p",
    "t_RISE" : "100p",
    "V_DD"   : "2.5"
  }

  with ocean.Ocean(fname=script_name, schematic=schematic,
                   path=path, simpath=simpath,
                   *args, **kwargs) as oc:
    for k, v in designVars.iteritems():
      oc.desVar(k, lispify.Atom(v))

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
  parser.add_argument('--modelfile', dest='modelfile',
                      type=str, default='tsmc025.m',
                      help='Model library technology file')

  args = parser.parse_args()
  main(**dict(args._get_kwargs()))
