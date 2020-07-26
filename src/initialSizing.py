from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from astropy import units as u

import roarCore.sizing as roarSizing


# spec: when it is a design spec
# input: when it is a input property (with less or no control over this)
# const: for universal physical constants
# choice: when the user has chosen a specific value


class SizingEngine:

    def __init__(self):
        self.choiceFuel = 'wax'
        self.choiceOx = 'nitrous'

        self.specTotalImpulse = 13500 * u.N * u.s
        self.specThrustAvg = 1500 * u.N

        self.inputOFDesign = 6
        self.inputIspDesign = 300 * u.s

        self.constg0 = 9.81 * u.m * u.s**-2

        self.inputUllageOx = 0.05
        self.inputUllageFuel = 0.05

        self.specThrustInit = 1500 * u.N
        self.inputIspInit = 300 * u.s

        self.inputOFInit = 6

        self.specPressureCombustionChamber = 30 * u.bar

        self.specInjectorPressureDropRatio = 0.15
        self.inputInjectorHeadLossCoeff = 1.5

        self.inputOxDensity = 1000 * u.kg/u.m**3  # TODO: implement

        self.inputMassFluxOx = 350 * u.kg / (u.m**2) / u.s

        self.choicePortType = 'circular'

        self.inputFuelDensitySolid = 900*u.kg/u.m**3

        # ASSUMES SI UNITS!
        self.inputRegressionParamsSI = {'a': 0.0000236, 'n': 0.605, 'm': 0}

        # TODO: Refactor these:
        self.inputTemperatureFlame = 3300 * u.Kelvin
        self.inputGamma = 1.28
        self.inputSpecificGasConstant = 280 * u.J / (u.kg * u.Kelvin)
        self.inputCombustionEfficiency = 0.93

        self.inputPressureExit = 1 * u.bar

    def size(self):

        self.compTimeBurn = roarSizing.computeBurnTime(
            totalImpulse=self.specTotalImpulse,
            avgThrust=self.specThrustAvg)

        self.compMassPropellant = roarSizing.computeMassPropellantRequired(
            totalImpulse=self.specTotalImpulse,
            specificImpulse=self.inputIspDesign,
            g0=self.constg0)

        self.compMassOx = roarSizing.computeMassOx(
            massPropellant=self.compMassPropellant,
            OF=self.inputOFDesign,
            ullage=self.inputUllageOx)

        self.compMassFuel = roarSizing.computeMassFuel(
            massPropellant=self.compMassPropellant,
            OF=self.inputOFDesign,
            ullage=self.inputUllageFuel)

        self.compMdotPropInit = roarSizing.computeMdotProp(
            thrust=self.specThrustInit,
            Isp=self.inputIspInit,
            g0=self.constg0
        )

        self.compMdotOxInit = roarSizing.computeMdotOx(
            mdotProp=self.compMdotPropInit,
            OF=self.inputOFInit
        )

        self.compMdotFuel = roarSizing.computeMdotFuel(
            mdotProp=self.compMdotPropInit,
            OF=self.inputOFInit
        )

        self.compPressureDropInjector = roarSizing.computePressureDropInjector(
            pressureCombustionChamber=self.specPressureCombustionChamber,
            pressureDropRatio=self.specInjectorPressureDropRatio
        )

        self.compInjectorArea = roarSizing.computeInjectorArea(
            mdotOx=self.compMdotOxInit,
            headLossCoeff=self.inputInjectorHeadLossCoeff,
            densityOxL=self.inputOxDensity,
            injectorPressureDrop=self.compPressureDropInjector
        )

        # for a single injector hole
        self.compInjectorDiameter = roarSizing.area_to_diameter(
            self.compInjectorArea).to(u.mm)

        self.compPortAreaInit = roarSizing.computePortArea(
            mdotOx=self.compMdotOxInit,
            oxFlux=self.inputMassFluxOx)

        if self.choicePortType == 'circular':

            self.compPortDiameterInit = roarSizing.area_to_diameter(
                self.compPortAreaInit).to(u.mm)

            self.compPortPerimeterInit = roarSizing.computePerimeterCircular(
                diameter=self.compPortDiameterInit)

        else:
            raise NotImplementedError(
                'Only the circular port calculations have been implemented')

        self.compGrainLength = roarSizing.computeGrainLength(
            mdotFuel=self.compMdotFuel,
            densityFuelS=self.inputFuelDensitySolid,
            oxFlux=self.inputMassFluxOx,
            perimeter=self.compPortPerimeterInit,
            regressionParams=self.inputRegressionParamsSI).to(u.mm)

        self.compPortDiameterFinal = roarSizing.computePortDiameterFinal(
            massFuel=self.compMassFuel,
            densityFuelS=self.inputFuelDensitySolid,
            grainLength=self.compGrainLength,
            portInitialDiameter=self.compPortDiameterInit).to(u.mm)

        self.compAreaCombustionChamber = roarSizing.diameter_to_area(
            diameter=self.compPortDiameterFinal)

        self.compRegressionRateInitial = roarSizing.computeRegressionRate(
            oxFlux=self.inputMassFluxOx,
            grainLength=self.compGrainLength,
            regressionParams=self.inputRegressionParamsSI).to(u.mm/u.s)

        self.compCharacteristicSpeed = roarSizing.computeCharacteristicSpeed(
            gamma=self.inputGamma,
            specificGasConstant=self.inputSpecificGasConstant,
            temperatureCombustionChamber=self.inputTemperatureFlame,
            combustionEfficiency=self.inputCombustionEfficiency)

        self.compAreaThroat = roarSizing.computeThroatArea(
            mdotProp=self.compMdotPropInit,
            characteristicSpeed=self.compCharacteristicSpeed,
            pressureCombustionChamber=self.specPressureCombustionChamber)

        self.compDiameterThroat = roarSizing.area_to_diameter(
            area=self.compAreaThroat).to(u.mm)

        self.compMachCombustionChamber = roarSizing.computeMachCombustionChamber(
            gamma=self.inputGamma,
            areaThroat=self.compAreaThroat,
            areaCombustion=self.compAreaCombustionChamber,
        )

        self.compMachExit = roarSizing.computeMachExit(
            gamma=self.inputGamma,
            pressureCombustionChamber=self.specPressureCombustionChamber,
            pressureExit=self.inputPressureExit
        )

        self.compTempExit = roarSizing.computeTemperatureExit(
            gamma=self.inputGamma,
            machExit=self.compMachExit,
            temperatureCombustionChamber=self.inputTemperatureFlame)

        self.compAreaRatioExit = roarSizing.expansionRatio(
            gamma=self.inputGamma,
            mach=self.compMachExit)

        self.compAreaExit = self.compAreaRatioExit * self.compAreaThroat

        self.compDiameterExit = roarSizing.area_to_diameter(
            area=self.compAreaExit).to(u.mm)

    def printTable(self):
        results = OrderedDict(sorted(self.__dict__.items()))

        dfResult = pd.DataFrame.from_dict(results, orient='index')

        print(dfResult)

        return dfResult


if __name__ == '__main__':

    print(" ~~ Roar Sizing Tool ~~")

    engine = SizingEngine()

    print("Starting Sizing...")

    engine.size()

    print("Sizing Successful !! ")

    engine.printTable()
