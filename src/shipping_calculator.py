"""
System obliczania kosztów wysyłki w sklepie internetowym.
UWAGA: Ten kod wymaga refaktoryzacji! Użyj wzorca Strategy.
"""
from typing import Dict, Tuple
from src.strategies import standard_shipping, express_shipping, drone_shipping, locker_shipping, economy_shipping, \
    same_day_shipping
from src.models.package import Package


class ShippingCalculator:
    """
    Kalkulator kosztów wysyłki.
    TODO: Ten kod to koszmar! Refaktoryzacja z użyciem Strategy Pattern.
    """
    
    def __init__(self):
        self.strategies = {
            "standard": standard_shipping.StandardShipping(),
            "express": express_shipping.ExpressShipping(),
            "same_day": same_day_shipping.SameDayShipping(),
            "economy": economy_shipping.EconomyShipping(),
            "drone": drone_shipping.DroneShipping(),
            "locker": locker_shipping.LockerShipping(),
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

        strategy = self.strategies.get(shipping_type)
        if not strategy:
            return {"cost": None, "delivery_date": None, "info": f"Nieznany typ dostawy: {shipping_type}"}
        return strategy.calculate(package, distance, customer_type)
        


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