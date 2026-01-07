from typing import Tuple

class Package:
    def __init__(self, weight: float, dimensions: Tuple[float, float, float],
                 value: float, is_fragile: bool = False):
        self.weight = weight
        self.dimensions = dimensions
        self.value = value
        self.is_fragile = is_fragile

    @property
    def volume(self):
        return self.dimensions[0] * self.dimensions[1] * self.dimensions[2] / 1_000_000
