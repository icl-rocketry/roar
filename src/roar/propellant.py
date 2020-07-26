# Propellant


class Propellant:

    def __init__(self, fuel, ox):
        self.fuel = fuel
        self.ox = ox

    def __repr__(self):
        return f'Propellant: {self.fuel}, {self.ox}'
