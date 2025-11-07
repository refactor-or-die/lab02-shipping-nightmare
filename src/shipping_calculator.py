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

    def __init__(self, base_rate: float):
        self.base_rate = base_rate

    @abstractmethod
    def calculate(self, package: Package, distance: float, customer_type: str) -> Dict:

        pass

    def apply_customer_discount(self, cost: float, customer_type: str,
                                premium_rate: float = 0.9, vip_rate: float = 0.8) -> float:
        if customer_type == "premium":
            return cost * premium_rate
        elif customer_type == "vip":
            return cost * vip_rate
        return cost


class StandardShippingStrategy(ShippingStrategy):


    def calculate(self, package: Package, distance: float, customer_type: str) -> Dict:
        base_cost = self.base_rate

        # Dodatkowe opłaty za wagę
        if package.weight > 20:
            base_cost += (package.weight - 20) * 5
        elif package.weight > 10:
            base_cost += (package.weight - 10) * 3
        elif package.weight > 5:
            base_cost += (package.weight - 5) * 2

        # Opłata za wymiary
        if package.volume > 0.1:
            base_cost += 20

        if distance > 100:
            base_cost += (distance - 100) * 0.1

        base_cost = self.apply_customer_discount(base_cost, customer_type)

        delivery_days = 3 if distance < 200 else 5

        return {
            "cost": round(base_cost, 2),
            "delivery_date": datetime.now() + timedelta(days=delivery_days),
            "info": "Standardowa dostawa kurierem"
        }


class ExpressShippingStrategy(ShippingStrategy):

    def calculate(self, package: Package, distance: float, customer_type: str) -> Dict:
        if package.weight > 15:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Express nie obsługuje paczek powyżej 15kg"
            }

        base_cost = self.base_rate

        if package.weight > 8:
            base_cost += (package.weight - 3) * 4 + (package.weight - 8) * 6
        elif package.weight > 3:
            base_cost += (package.weight - 3) * 4

        base_cost += distance * 0.2

        if package.is_fragile:
            base_cost += 15

        base_cost = self.apply_customer_discount(base_cost, customer_type, 0.95, 0.85)

        delivery_days = 1 if distance < 300 else 2

        return {
            "cost": round(base_cost, 2),
            "delivery_date": datetime.now() + timedelta(days=delivery_days),
            "info": "Ekspresowa dostawa - priorytet"
        }


class SameDayShippingStrategy(ShippingStrategy):

    def calculate(self, package: Package, distance: float, customer_type: str) -> Dict:
        if distance > 50:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Same day delivery dostępne tylko do 50km"
            }

        if package.weight > 10:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Same day nie obsługuje paczek powyżej 10kg"
            }

        base_cost = self.base_rate

        if package.weight > 5:
            base_cost += 30

        current_hour = datetime.now().hour
        if current_hour > 14:
            base_cost += 20  # Po 14:00 drożej

        if customer_type == "vip":
            base_cost = 0
        elif customer_type == "premium":
            base_cost *= 0.7

        return {
            "cost": round(base_cost, 2),
            "delivery_date": datetime.now(),
            "info": "Dostawa tego samego dnia!"
        }


class EconomyShippingStrategy(ShippingStrategy):

    def calculate(self, package: Package, distance: float, customer_type: str) -> Dict:
        if package.is_fragile:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Economy nie obsługuje przesyłek delikatnych"
            }

        base_cost = self.base_rate

        if package.weight < 1:
            base_cost = 8
        else:
            base_cost += package.weight * 1.5

        if distance > 500:
            base_cost *= 0.8

        delivery_days = random.randint(5, 10)  # Nieprzewidywalny czas

        return {
            "cost": round(base_cost, 2),
            "delivery_date": datetime.now() + timedelta(days=delivery_days),
            "info": f"Ekonomiczna dostawa (5-10 dni)"
        }


class InternationalStandardShippingStrategy(ShippingStrategy):

    def calculate(self, package: Package, distance: float, customer_type: str) -> Dict:
        base_cost = self.base_rate

        customs = package.value * 0.23 if package.value > 150 else 0
        base_cost += customs

        if package.weight > 20:
            base_cost += (package.weight - 20) * 12
        elif package.weight > 2:
            base_cost += (package.weight - 2) * 8

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

        base_cost = self.apply_customer_discount(base_cost, customer_type, 0.85, 0.7)

        return {
            "cost": round(base_cost, 2),
            "delivery_date": datetime.now() + timedelta(days=delivery_days),
            "info": f"Dostawa międzynarodowa ({zone}) - cło wliczone"
        }


class InternationalExpressShippingStrategy(ShippingStrategy):

    def calculate(self, package: Package, distance: float, customer_type: str) -> Dict:
        base_cost = self.base_rate

        customs = package.value * 0.23 if package.value > 150 else 0
        base_cost += customs

        if package.weight > 2:
            base_cost += (package.weight - 2) * 12

        if distance < 1000:
            zone = "EU"
            delivery_days = 3
        elif distance < 5000:
            zone = "Europe"
            base_cost *= 1.5
            delivery_days = 7
        else:
            zone = "World"
            base_cost *= 2.5
            delivery_days = 10

        base_cost = self.apply_customer_discount(base_cost, customer_type, 0.85, 0.7)

        return {
            "cost": round(base_cost, 2),
            "delivery_date": datetime.now() + timedelta(days=delivery_days),
            "info": f"Ekspresowa dostawa międzynarodowa ({zone})"
        }


class DroneShippingStrategy(ShippingStrategy):

    def calculate(self, package: Package, distance: float, customer_type: str) -> Dict:
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

        base_cost = self.base_rate

        weather_penalty = random.choice([0, 10, 20, 50])
        if weather_penalty == 50:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Złe warunki pogodowe - drony nie latają"
            }

        base_cost += weather_penalty

        if customer_type in ["premium", "vip"]:
            base_cost *= 0.5
            delivery_time = 30
        else:
            delivery_time = 60

        return {
            "cost": round(base_cost, 2),
            "delivery_date": datetime.now() + timedelta(minutes=delivery_time),
            "info": f"Dostawa dronem w {delivery_time} minut!"
        }


class LockerShippingStrategy(ShippingStrategy):

    def calculate(self, package: Package, distance: float, customer_type: str) -> Dict:
        if package.weight > 25:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Paczkomaty obsługują maksymalnie 25kg"
            }

        max_dim = max(package.dimensions)
        if max_dim > 60:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Paczka za duża do paczkomatu"
            }

        base_cost = self.base_rate

        if distance > 50:
            base_cost += 3

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
            "standard": StandardShippingStrategy(15),
            "express": ExpressShippingStrategy(30),
            "same_day": SameDayShippingStrategy(50),
            "economy": EconomyShippingStrategy(10),
            "international_standard": InternationalStandardShippingStrategy(45),
            "international_express": InternationalExpressShippingStrategy(80),
            "drone": DroneShippingStrategy(40),
            "locker": LockerShippingStrategy(12)
        }

    def calculate_shipping(self, package: Package, shipping_type: str,
                           distance: float, customer_type: str = "regular") -> Dict:

        strategy = self.strategies.get(shipping_type)

        if strategy is None:
            return {
                "cost": None,
                "delivery_date": None,
                "info": f"Nieznany typ dostawy: {shipping_type}"
            }

        return strategy.calculate(package, distance, customer_type)

    def add_shipping_strategy(self, name: str, strategy: ShippingStrategy):
        self.strategies[name] = strategy


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