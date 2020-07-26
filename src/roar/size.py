# roar.size provides helper functions for sizing engines.

def computeBurnTime(totalImpulse, avgThrust):
    return totalImpulse/avgThrust.si


def computeMassPropellantRequired(totalImpulse, specificImpulse, g0):
    return totalImpulse/(specificImpulse * g0).si


def computeMassOx(massPropellant, OF, ullage=0):
    return (1+ullage) * massPropellant * OF / (OF + 1)


def computeMassFuel(massPropellant, OF, ullage=0):
    return (1+ullage) * massPropellant / (OF + 1)
