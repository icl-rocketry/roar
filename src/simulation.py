# Size and Simulate Script
import numpy as np
from scipy.optimize import root
import matplotlib.pyplot as plt
from astropy import units as u

import roarCore.sizing as roarSize
import roarCore.simulate as roarSim

import initialSizing

def find_Gprop(G_ox, rho_fuel, portLength, a, n, m):

  # bind the values to the function
  # using a vector valued function here, with just one component.
  def errorFunc(x):

    G_prop = x[0]

    # compute the error
    err = (G_ox  + rho_fuel * portLength * a * G_prop**n * portLength**m) - G_prop

    return [err]

  initialGuess = [G_ox/2]
  sol = root(errorFunc, initialGuess) # using scipy.optimize.root

  return sol.x


def simulate(engine, timestep=0.01*u.s):

  # load initial values
  portLength = engine.compGrainLength
  portDiameter = engine.compPortDiameterInit
  mdot_ox = engine.compMdotOxInit
  rho_fuel = engine.inputFuelDensitySolid

  a = engine.inputRegressionParamsSI['a']
  n = engine.inputRegressionParamsSI['n']
  m = engine.inputRegressionParamsSI['m']

  ## set up simulation
  done = False

  t = 0
  ti = 0
  dt = timestep

  while not done:
    
    ## STEP 2 - mass flow rates and regression rate
    portArea = roarSize.diameter_to_area(portDiameter)
    portPerimeter = roarSize.diameter_to_perimeter(portDiameter)
    portSurfaceArea = portPerimeter * portLength

    G_ox = mdot_ox / portArea
  
    G_prop = find_Gprop(G_ox, rho_fuel, portLength, a, n, m)

    G_fuel = G_prop - G_ox
    rdot = a * G_prop ** n * portLength ** m

    mdot_fuel = rdot * rho_fuel * portSurfaceArea

    mdot_prop = mdot_fuel + mdot_ox

    ## STEP 3 - thermochemistry

    c_star 

    OF = mdot_ox / mdot_fuel

    T_stagnation = T_flame # poor assumption!

    P_cc = mdot_prop * c_star / A_throat



    ## STEP 4 - Nozzle Flow

    ## STEP 5 - Estimate force and Isp

    ## STEP 6 - Check if finsihed

    

# Done Simulation

  print("WEEEEE")

  return None



if __name__ == '__main__':
  
  eng = initialSizing.SizingEngine() # create an engine
  eng.size()

  simResult = simulate(eng)

  print(simResult)
