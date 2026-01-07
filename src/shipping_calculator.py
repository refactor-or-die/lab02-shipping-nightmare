"""
System obliczania kosztów wysyłki w sklepie internetowym.
UWAGA: Ten kod wymaga refaktoryzacji! Użyj wzorca Strategy.
"""
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

from abc import ABC, abstractmethod
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

class ShippingStrategy(ABC):
    @abstractmethod
    def calculate(self, package: List[Package], distance: float, customer_type: str = "regular") -> dict:
        pass

class StandardStrategy(ShippingStrategy):
    def calculate(self, package: List[Package], distance: float, customer_type: str = "regular") -> dict:
        base_cost = 15

        # Dodatkowe opłaty za wagę
        if package.weight > 5:
            base_cost += (package.weight - 5) * 2
        elif package.weight > 10:
            base_cost += (package.weight - 10) * 3
        elif package.weight > 20:
            base_cost += (package.weight - 20) * 5

        # Opłata za wymiary
        if package.volume > 0.1:
            base_cost += 20

        # Opłata za dystans
        if distance > 100:
            base_cost += (distance - 100) * 0.1

        # Rabat dla klientów
        if customer_type == "premium":
            base_cost *= 0.9
        elif customer_type == "vip":
            base_cost *= 0.8

        delivery_days = 3 if distance < 200 else 5

        return {
            "cost": round(base_cost, 2),
            "delivery_date": datetime.now() + timedelta(days=delivery_days),
            "info": "Standardowa dostawa kurierem"
        }


class ExpressStrategy(ShippingStrategy):
    def calculate(self, package: List[Package], distance: float, customer_type: str = "regular") -> dict:
        base_cost = 30
        # Express nie przyjmuje powyżej 15kg
        if package.weight > 15:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Express nie obsługuje paczek powyżej 15kg"
            }

        # Express ma inne progi wagowe
        if package.weight > 8:
            base_cost += (package.weight - 3) * 4 + (package.weight - 8) * 6
        elif package.weight > 3:
            base_cost += (package.weight - 3) * 4

        # Express ma wyższą opłatę za dystans
        base_cost += distance * 0.2

        # Opłata za przesyłki delikatne
        if package.is_fragile:
            base_cost += 15

        # Rabaty
        if customer_type == "premium":
            base_cost *= 0.95
        elif customer_type == "vip":
            base_cost *= 0.85

        delivery_days = 1 if distance < 300 else 2

        return {
            "cost": round(base_cost, 2),
            "delivery_date": datetime.now() + timedelta(days=delivery_days),
            "info": "Ekspresowa dostawa - priorytet"
        }

class SameDayStrategy(ShippingStrategy):
    def calculate(self, package: List[Package], distance: float, customer_type: str = "regular") -> dict:
        base_cost = 50
        if distance > 50:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Same day delivery dostępne tylko do 50km"
            }



        # Same day ma stałą opłatę za wagę
        if package.weight > 5:
            base_cost += 30
        elif package.weight > 10:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Same day nie obsługuje paczek powyżej 10kg"
            }

        # Dodatkowa opłata za porę dnia
        current_hour = datetime.now().hour
        if current_hour > 14:
            base_cost += 20  # Po 14:00 drożej

        # VIP ma darmową dostawę same day!
        if customer_type == "vip":
            base_cost = 0
        elif customer_type == "premium":
            base_cost *= 0.7

        return {
            "cost": round(base_cost, 2),
            "delivery_date": datetime.now(),
            "info": "Dostawa tego samego dnia!"
        }


class EconomyStrategy(ShippingStrategy):
    def calculate(self, package: List[Package], distance: float, customer_type: str = "regular") -> dict:
        base_cost = 10

        # Economy ma minimalną opłatę
        if package.weight < 1:
            base_cost = 8
        else:
            base_cost += package.weight * 1.5

        # Nie dostarczamy przesyłek delikatnych economy
        if package.is_fragile:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Economy nie obsługuje przesyłek delikatnych"
            }

        # Im dalej tym taniej (transport zbiorczy)
        if distance > 500:
            base_cost *= 0.8

        # Brak rabatów dla economy
        delivery_days = random.randint(5, 10)  # Nieprzewidywalny czas

        return {
            "cost": round(base_cost, 2),
            "delivery_date": datetime.now() + timedelta(days=delivery_days),
            "info": f"Ekonomiczna dostawa (5-10 dni)"
        }


class InternationalStandardStrategy(ShippingStrategy):
    def calculate(self, package: List[Package], distance: float, customer_type: str = "regular") -> dict:
        base_cost = 45
        # Opłaty celne symulowane
        customs = package.value * 0.23 if package.value > 150 else 0
        base_cost += customs

        # Waga międzynarodowa
        if package.weight > 2:
            base_cost += (package.weight - 2) * 8
        elif package.weight > 20:
            base_cost += (package.weight - 20) * 12

        # Strefa dostaw
        if distance < 1000:
            zone = "EU"
            delivery_days = 7
        elif distance < 5000:
            zone = "Europe"
            base_cost *= 1.5
            delivery_days = 14
        else:
            zone = "World"
            base_cost *= 2.5
            delivery_days = 21

        # Rabaty międzynarodowe
        if customer_type == "vip":
            base_cost *= 0.7
        elif customer_type == "premium":
            base_cost *= 0.85

        return {
            "cost": round(base_cost, 2),
            "delivery_date": datetime.now() + timedelta(days=delivery_days),
            "info": f"Dostawa międzynarodowa ({zone}) - cło wliczone"
        }

class InternationalExpressStrategy(ShippingStrategy):
    def calculate(self, package: List[Package], distance: float, customer_type: str = "regular") -> dict:
        base_cost = 80

class DroneStrategy(ShippingStrategy):
    def calculate(self, package: List[Package], distance: float, customer_type: str = "regular") -> dict:
        base_cost = 40
        if package.weight > 2:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Drony obsługują tylko paczki do 2kg"
            }

        if distance > 20:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Zasięg dronów to maksymalnie 20km"
            }


        weather_penalty = random.choice([0, 10, 20, 50])
        if weather_penalty == 50:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Złe warunki pogodowe - drony nie latają"
            }

        base_cost += weather_penalty

        # Premium i VIP mają priorytet
        if customer_type in ["premium", "vip"]:
            base_cost *= 0.5
            delivery_time = 30  # minut
        else:
            delivery_time = 60  # minut

        return {
            "cost": round(base_cost, 2),
            "delivery_date": datetime.now() + timedelta(minutes=delivery_time),
            "info": f"Dostawa dronem w {delivery_time} minut!"
        }

class LockerStrategy(ShippingStrategy):
    def calculate(self, package: List[Package], distance: float, customer_type: str = "regular") -> dict:
        base_cost = 12

        # Paczkomaty mają limity
        if package.weight > 25:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Paczkomaty obsługują maksymalnie 25kg"
            }

        # Sprawdzenie wymiarów
        max_dim = max(package.dimensions)
        if max_dim > 60:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Paczka za duża do paczkomatu"
            }

        # Stała opłata niezależnie od wagi
        if distance > 50:
            base_cost += 3

        # VIP ma darmowe paczkomaty
        if customer_type == "vip":
            base_cost = 0
        elif customer_type == "premium":
            base_cost *= 0.8

        delivery_days = 1 if distance < 200 else 2

        return {
            "cost": round(base_cost, 2),
            "delivery_date": datetime.now() + timedelta(days=delivery_days),
            "info": "Dostawa do paczkomatu"
        }






class ShippingCalculator:

    
    def __init__(self):
        self.strategies = {
            "standard": StandardStrategy(),
            "express":  ExpressStrategy(),
            "same_day": SameDayStrategy(),
            "economy": EconomyStrategy(),
            "international_standard": InternationalStandardStrategy(),
            "international_express": InternationalExpressStrategy(),
            "drone": DroneStrategy(),
            "locker": LockerStrategy(),
        }
    
    def calculate_shipping(self, package: Package, shipping_type: str, 
                         distance: float, customer_type: str = "regular") -> Dict:
        strategy = self.strategies[shipping_type]

        if not strategy:
            return {
                "cost": None,
                "delivery_date": None,
                "info" : f"Nieznany typ dostawy: {shipping_type}"
            }



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