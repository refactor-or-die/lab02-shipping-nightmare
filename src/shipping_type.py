from abc import ABC, abstractmethod

from .package import  Package

class ShippingType(ABC):
    @abstractmethod
    def calculate(self, package: Package, distance: float, customer_type: str) -> dict:
        pass