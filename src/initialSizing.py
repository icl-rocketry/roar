import numpy as np
import matplotlib.pyplot as plt

from astropy import units as u

import roar.size as roar


# spec: when it is a design spec
# input: when it is a input property (with less or no control over this)
# const: for universal physical constants


class Engine:

    def __init__(self):
        self.fuel = 'wax'
        self.ox = 'nitrous'

        self.specTotalImpulse = 13500 * u.N * u.s
        self.specAvgThrust = 1500 * u.N

        self.inputDesignOF = 8
        self.inputDesignIsp = 300 * u.s

        self.constg0 = 9.81 * u.m * u.s**-2

        self.inputUllageOx = 0.05
        self.inputUllageFuel = 0.05

    def size(self):

        self.compBurnTime = roar.computeBurnTime(
            totalImpulse=self.specTotalImpulse,
            avgThrust=self.specAvgThrust)

        self.compMassPropellant = roar.computeMassPropellantRequired(
            totalImpulse=self.specTotalImpulse,
            specificImpulse=self.inputDesignIsp,
            g0=self.constg0)

        self.compMassOx = roar.computeMassOx(
            massPropellant=self.compMassPropellant,
            OF=self.inputDesignOF,
            ullage=self.inputUllageOx)

        self.compMassFuel = roar.computeMassFuel(
            massPropellant=self.compMassPropellant,
            OF=self.inputDesignOF,
            ullage=self.inputUllageFuel)


if __name__ == '__main__':

    engine = Engine()

    engine.size()

    for key in sorted(engine.__dict__):
        try:
            print(key, ' -> ', engine.__dict__[key].si)
        except:
            print(key, ' -> ', engine.__dict__[key])
