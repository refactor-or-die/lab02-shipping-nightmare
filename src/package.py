class Package:
    """Paczka do wysyłki"""

    def __init__(self, weight: float, dimensions: tuple[float, float, float],
                 value: float, is_fragile: bool = False):
        self.weight = weight  # kg
        self.dimensions = dimensions  # (length, width, height) in cm
        self.value = value  # PLN
        self.is_fragile = is_fragile

    @property
    def volume(self):
        return self.dimensions[0] * self.dimensions[1] * self.dimensions[2] / 1000000  # m³
