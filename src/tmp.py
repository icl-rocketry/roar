import numpy as np
from scipy.optimize import root_scalar

G_ox = 350
a = 2.36 * 1e-05
n = 0.605
m = 0

L = 0.790

rho_fuel = 900


portD = 39.8 * 1e-3
portA = np.pi * portD**2/4
SA = (np.pi * portD) * L # surface Area

def func(G_fuel):
  print(f'Trying x: {G_fuel}')

  G_prop = G_fuel + G_ox
  rdot = a * G_prop**n * L**m
  mdot_fuel = rdot * rho_fuel * SA
  err = G_fuel - mdot_fuel/portA

  print(f'Error: {err}')
  return err

sol = root_scalar(func, method='secant', x0=G_ox/2, x1=0)

print(sol)

