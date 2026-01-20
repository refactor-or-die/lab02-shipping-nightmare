"""
System obliczania kosztów wysyłki w sklepie internetowym.
UWAGA: Ten kod wymaga refaktoryzacji! Użyj wzorca Strategy.
"""
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from shipping_type_factory import ShippingTypeFactory
from shipping_type import *


class Package:
    """Paczka do wysyłki"""
    def __init__(self, weight: float, dimensions: Tuple[float, float, float], 
                 value: float, is_fragile: bool = False):
        self.weight = weight  # kg
        self.dimensions = dimensions  # (length, width, height) in cm
        self.value = value  # PLN
        self.is_fragile = is_fragile
    
    @property
    def volume(self):
        return self.dimensions[0] * self.dimensions[1] * self.dimensions[2] / 1000000  # m³


class ShippingCalculator:
    """
    Kalkulator kosztów wysyłki.
    TODO: Ten kod to koszmar! Refaktoryzacja z użyciem Strategy Pattern.
    """
    
    def __init__(self):
        self.base_rates = {
            "standard": 15,
            "express": 30,
            "same_day": 50,
            "economy": 10,
            "international_standard": 45,
            "international_express": 80,
            "drone": 40,
            "locker": 12
        }
    
    def calculate_shipping(self, package: Package, shipping_type: str, 
                         distance: float, customer_type: str = "regular") -> Dict:
        """
        Oblicza koszt wysyłki.
        
        Args:
            package: Paczka do wysyłki
            shipping_type: Typ wysyłki
            distance: Odległość w km
            customer_type: "regular", "premium", "vip"
            
        Returns:
            Dict z kosztem, czasem dostawy i dodatkową informacją
        """
        
        # Ten if-else nightmare kończy się tutaj...

        factory = ShippingTypeFactory()
        shippingType = factory.create(shipping_type)

        if (isinstance(shippingType, UnknownShipping)):
            return {
                "cost": None,
                "delivery_date": None,
                "info": f"Nieznany typ dostawy: {shipping_type}"
            }
            
        elif (isinstance(shippingType, ShippingType)):
            return shippingType.calculateShipping(package, distance, customer_type)
            

# Przykład użycia
if __name__ == "__main__":
    calculator = ShippingCalculator()
    
    # Testowe paczki
    small_package = Package(0.5, (20, 15, 10), 50)
    medium_package = Package(5, (40, 30, 20), 200, is_fragile=True)
    large_package = Package(15, (60, 50, 40), 500)
    
    # Test różnych typów dostaw
    shipping_types = ["standard", "express", "same_day", "economy", 
                     "international_standard", "drone", "locker"]
    
    print("=== KALKULATOR KOSZTÓW WYSYŁKI ===\n")
    
    for package, desc in [(small_package, "Mała paczka"), 
                          (medium_package, "Średnia (delikatna)"),
                          (large_package, "Duża paczka")]:
        print(f"\n{desc}: {package.weight}kg, {package.value}PLN")
        print("-" * 50)
        
        for shipping in shipping_types:
            result = calculator.calculate_shipping(package, shipping, 100, "regular")
            if result["cost"] is not None:
                print(f"{shipping:20} {result['cost']:8.2f} PLN - {result['info']}")
            else:
                print(f"{shipping:20} NIEDOSTĘPNE - {result['info']}")
