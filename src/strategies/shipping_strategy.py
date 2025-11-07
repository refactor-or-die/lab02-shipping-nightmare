from abc import ABC, abstractmethod
from src.models.package import Package
from typing import Dict

class ShippingStrategy(ABC):
    @abstractmethod
    def calculate(self, package: Package, distance: float, customer_type: str = "regular") -> Dict:
        pass
