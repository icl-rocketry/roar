'''

roar.size provides helper functions for sizing engines.

See
https://devanshinspace.gitbook.io/roar/hybrid-engines/background-on-hybrids/sizing-a-hybrid
for explanation of each of the function
'''

from astropy import units as u
import numpy as np
from scipy import optimize as opt


# define helper units
uFlux = u.kg / (u.m**2) / u.s


def si(func):
    '''
    Helper function to return everything in SI version of units
    '''
    def wrapperFunc(*args, **kwargs):
        return func(*args, **kwargs).si

    return wrapperFunc


@si
@u.quantity_input
def computeBurnTime(
        totalImpulse: u.N*u.s,
        avgThrust: u.N) -> u.s:

    return totalImpulse/avgThrust


@si
@u.quantity_input
def computeMassPropellantRequired(
        totalImpulse: u.N * u.s,
        specificImpulse: u.s,
        g0: u.m/u.s/u.s) -> u.kg:

    return totalImpulse/(specificImpulse * g0)


@u.quantity_input
def computeMassOx(
        massPropellant: u.kg,
        OF,
        ullage=0) -> u.kg:

    return (1+ullage) * massPropellant * OF / (OF + 1)


@u.quantity_input
def computeMassFuel(
        massPropellant: u.kg,
        OF, ullage=0) -> u.kg:

    return (1+ullage) * massPropellant / (OF + 1)


@si
@u.quantity_input
def computeMdotProp(
        thrust: u.N,
        Isp: u.s,
        g0: u.m/u.s/u.s) -> u.kg/u.s:

    return (thrust/(Isp * g0))


@si
@u.quantity_input
def computeMdotOx(
        mdotProp: u.kg/u.s,
        OF) -> u.kg/u.s:

    return mdotProp * OF / (OF + 1)


@ si
@ u.quantity_input
def computeMdotFuel(
        mdotProp: u.kg/u.s,
        OF) -> u.kg/u.s:

    return mdotProp / (OF + 1)


@u.quantity_input
def computePressureDropInjector(
        pressureCombustionChamber: u.Pa,
        pressureDropRatio) -> u.bar:

    return pressureCombustionChamber * pressureDropRatio


@si
@u.quantity_input
def computeInjectorArea(
        mdotOx: u.kg/u.s,
        headLossCoeff,
        densityOxL: u.kg/u.m**3,
        injectorPressureDrop: u.Pa) -> u.m**2:

    A = mdotOx * (headLossCoeff / (2 * densityOxL * injectorPressureDrop))**0.5
    return A


@si
@u.quantity_input
def area_to_diameter(
        area: u.m**2) -> u.m:

    return 2 * (area/np.pi)**0.5


@si
@u.quantity_input
def diameter_to_area(
        diameter: u.m) -> u.m**2:

    return np.pi * diameter**2 / 4

@si
@u.quantity_input
def diameter_to_perimeter(diameter: u.m) -> u.m:

    return np.pi * diameter


@si
@u.quantity_input
def computePortArea(
        mdotOx: u.kg/u.s,
        oxFlux: uFlux) -> u.m**2:

    return mdotOx / oxFlux


@si
@u.quantity_input
def computePerimeterCircular(
        diameter: u.m) -> u.m:

    return np.pi * diameter


@si
@u.quantity_input
def computeGrainLength(
        mdotFuel: u.kg/u.s,
        densityFuelS: u.kg/u.m**3,
        oxFlux: uFlux,
        perimeter: u.m,
        regressionParams) -> u.m:

    a = regressionParams['a']
    n = regressionParams['n']
    m = regressionParams['m']

    # covert to si
    mdotFuel = mdotFuel.si.value
    densityFuelS = densityFuelS.si.value
    oxFlux = oxFlux.si.value
    perimeter = perimeter.si.value

    L = (mdotFuel / (a * densityFuelS * oxFlux**n * perimeter)) ** (1/(m+1))

    return L * u.m


@si
@u.quantity_input
def computePortDiameterFinal(
        massFuel: u.kg,
        densityFuelS: u.kg/u.m**3,
        grainLength: u.m,
        portInitialDiameter: u.m) -> u.m:

    d = ((4 * massFuel) / (np.pi * grainLength *
                           densityFuelS) + portInitialDiameter**2) ** 0.5

    return d


@si
@u.quantity_input
def computeRegressionRate(
        oxFlux: uFlux,
        grainLength: u.m,
        regressionParams) -> u.m/u.s:

    a = regressionParams['a']
    n = regressionParams['n']
    m = regressionParams['m']

    # covert to si
    oxFlux = oxFlux.si.value
    grainLength = grainLength.si.value

    r = a * oxFlux**n * grainLength ** m

    return r * u.m/u.s


@si
@u.quantity_input
def computeCharacteristicSpeed(
        gamma,
        specificGasConstant: u.J / (u.kg * u.Kelvin),
        temperatureCombustionChamber: u.Kelvin,
        combustionEfficiency=1) -> u.m/u.s:

    a = (gamma * specificGasConstant * temperatureCombustionChamber) ** 0.5
    b = combustionEfficiency * gamma * \
        (2 / (gamma+1)) ** ((gamma+1)/(2*gamma-2))

    c = a/b

    return c


@si
@u.quantity_input
def computeThroatArea(
        mdotProp: u.kg/u.s,
        characteristicSpeed: u.m/u.s,
        pressureCombustionChamber: u.Pa) -> u.m**2:

    return mdotProp * characteristicSpeed / pressureCombustionChamber


@u.quantity_input
def computeMachCombustionChamber(
        gamma,
        areaThroat: u.m**2 = None,
        areaCombustion: u.m**2 = None,
        diameterThroat: u.m = None,
        diameterCombustion: u.m = None):

    if ((areaThroat is None) and (diameterThroat is not None)):
        areaThroat = diameter_to_area(diameterThroat)

    if ((areaCombustion is None) and (diameterCombustion is not None)):
        areaCombustion = diameter_to_area(diameterCombustion)

    expR = (areaCombustion/areaThroat).decompose().value

    def func(M):
        return expansionRatio(mach=M, gamma=gamma) - expR

    sol = opt.root_scalar(func, bracket=(0.001, 0.999), method='brentq')

    if sol.converged:
        return sol.root

    print(sol)
    raise "Root finding for combustion chamber mach number failed to converge"


@si
@u.quantity_input
def computeTemperatureExit(
        gamma,
        machExit,
        temperatureCombustionChamber: u.Kelvin) -> u.Kelvin:

    return temperatureCombustionChamber * (1 + (gamma-1)/2 * machExit**2)**-1


def expansionRatio(mach, gamma):
    return (1/mach) * ((2/(gamma+1)) * (1 + (gamma-1)/2 * mach**2)) ** ((gamma+1)/(2 * gamma - 2))


@u.quantity_input
def computeMachExit(
        gamma,
        pressureCombustionChamber: u.Pa,
        pressureExit: u.Pa):

    pratio = (pressureCombustionChamber/pressureExit).decompose().value

    return (2/(gamma-1)) * (pratio ** ((gamma-1)/gamma) - 1)
