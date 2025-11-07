"""
System obliczania kosztów wysyłki w sklepie internetowym.
UWAGA: Ten kod wymaga refaktoryzacji! Użyj wzorca Strategy.
"""
import random
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, Tuple


class Package:
    def __init__(self, weight: float, dimensions: Tuple[float, float, float],
                 value: float, is_fragile: bool = False):
        self.weight = weight  
        self.dimensions = dimensions
        self.value = value
        self.is_fragile = is_fragile

    @property
    def volume(self):
        return self.dimensions[0] * self.dimensions[1] * self.dimensions[2] / 1000000  # m³

    @property
    def max_dimension(self):
        return max(self.dimensions)

class ShippingStrategy(ABC):
    @abstractmethod
    def calculate_cost(self, package: Package, distance: float, customer_type: str) -> Dict:
        pass

class StandardShippingStrategy(ShippingStrategy):
    def __init__(self):
        self.base_rate = 15

    def calculate_cost(self, package: Package, distance: float, customer_type: str) -> Dict:
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

        # Opłata za dystans
        if distance > 100:
            base_cost += (distance - 100) * 0.1

        # Rabat dla klientów
        discounts = {"regular": 1.0, "premium": 0.9, "vip": 0.8}
        final_cost = base_cost * discounts.get(customer_type, 1.0)

        delivery_days = 3 if distance < 200 else 5

        return {
            "cost": round(final_cost, 2),
            "delivery_date": datetime.now() + timedelta(days=delivery_days),
            "info": "Standardowa dostawa kurierem"
        }

class ExpressShippingStrategy(ShippingStrategy):
    def __init__(self):
        self.base_rate = 30

    def calculate_cost(self, package: Package, distance: float, customer_type: str) -> Dict:

        # Express nie przyjmuje powyżej 15kg
        if package.weight > 15:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Express nie obsługuje paczek powyżej 15kg"
            }

        base_cost = self.base_rate

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
        express_discounts = {"regular": 1.0, "premium": 0.95, "vip": 0.85}
        final_cost = base_cost * express_discounts.get(customer_type, 1.0)

        delivery_days = 1 if distance < 300 else 2

        return {
            "cost": round(final_cost, 2),
            "delivery_date": datetime.now() + timedelta(days=delivery_days),
            "info": "Ekspresowa dostawa - priorytet"
        }

class SameDayShippingStrategy(ShippingStrategy):
    def __init__(self):
        self.base_rate = 50

    def calculate_cost(self, package: Package, distance: float, customer_type: str) -> Dict:
        # Same day tylko do 50km
        if distance > 50:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Same day delivery dostępne tylko do 50km"
            }

        # Same day ma stałą opłatę za wagę
        if package.weight > 10:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Same day nie obsługuje paczek powyżej 10kg"
            }

        base_cost = self.base_rate

        if package.weight > 5:
            base_cost += 30

        # Dodatkowa opłata za porę dnia
        current_hour = datetime.now().hour
        if current_hour > 14:
            base_cost += 20

        # VIP ma darmową dostawę same day!
        if customer_type == "vip":
            base_cost = 0  # VIP ma darmową dostawę same day!
        elif customer_type == "premium":
            base_cost *= 0.7

        return {
            "cost": round(base_cost, 2),
            "delivery_date": datetime.now(),
            "info": "Dostawa tego samego dnia!"
        }

class EconomyShippingStrategy(ShippingStrategy):
    def __init__(self):
        self.base_rate = 10

    def calculate_cost(self, package: Package, distance: float, customer_type: str) -> Dict:
        # Nie dostarczamy przesyłek delikatnych economy
        if package.is_fragile:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Economy nie obsługuje przesyłek delikatnych"
            }

        # Economy ma minimalną opłatę
        if package.weight < 1:
            base_cost = 8
        else:
            base_cost = self.base_rate + package.weight * 1.5

        # Im dalej tym taniej (transport zbiorczy)
        if distance > 500:
            base_cost *= 0.8

        # Brak rabatów dla economy
        delivery_days = random.randint(5, 10)

        return {
            "cost": round(base_cost, 2),
            "delivery_date": datetime.now() + timedelta(days=delivery_days),
            "info": f"Ekonomiczna dostawa ({delivery_days} dni)"
        }

class InternationalStandardShippingStrategy(ShippingStrategy):
    def __init__(self):
        self.base_rate = 45

    def calculate_cost(self, package: Package, distance: float, customer_type: str) -> Dict:
        base_cost = self.base_rate

        # Opłaty celne symulowane
        customs = package.value * 0.23 if package.value > 150 else 0
        base_cost += customs

        # Waga międzynarodowa
        if package.weight > 20:
            base_cost += (package.weight - 20) * 12
        elif package.weight > 2:
            base_cost += (package.weight - 2) * 8

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
        intl_discounts = {"regular": 1.0, "premium": 0.85, "vip": 0.7}
        final_cost = base_cost * intl_discounts.get(customer_type, 1.0)

        return {
            "cost": round(final_cost, 2),
            "delivery_date": datetime.now() + timedelta(days=delivery_days),
            "info": f"Dostawa międzynarodowa ({zone}) - cło wliczone"
        }


class DroneShippingStrategy(ShippingStrategy):
    def __init__(self):
        self.base_rate = 40

    def calculate_cost(self, package: Package, distance: float, customer_type: str) -> Dict:
        # Drone delivery - przyszłość!
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

        # Warunki pogodowe (symulacja)
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


class LockerShippingStrategy(ShippingStrategy):
    def __init__(self):
        self.base_rate = 12

    def calculate_cost(self, package: Package, distance: float, customer_type: str) -> Dict:
        # Paczkomaty mają limity
        if package.weight > 25:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Paczkomaty obsługują maksymalnie 25kg"
            }

        # Sprawdzenie wymiarów
        if package.max_dimension > 60:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Paczka za duża do paczkomatu"
            }

        base_cost = self.base_rate

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
            "standard": StandardShippingStrategy(),
            "express": ExpressShippingStrategy(),
            "same_day": SameDayShippingStrategy(),
            "economy": EconomyShippingStrategy(),
            "international_standard": InternationalStandardShippingStrategy(),
            "drone": DroneShippingStrategy(),
            "locker": LockerShippingStrategy()
        }

    def calculate_shipping(self, package: Package, shipping_type: str,
                           distance: float, customer_type: str = "regular") -> Dict:
        strategy = self.strategies.get(shipping_type)
        if not strategy:
            return {
                "cost": None,
                "delivery_date": None,
                "info": f"Nieznany typ dostawy: {shipping_type}"
            }

        return strategy.calculate_cost(package, distance, customer_type)

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

    print("=== KALKULATOR KOSZTÓW WYSYŁKI (z ABC) ===\n")

    for package, desc in [(small_package, "Mała paczka"),
                          (medium_package, "Średnia (delikatna)"),
                          (large_package, "Duża paczka")]:
        print(f"\n{desc}: {package.weight}kg, {package.value}PLN")
        print("-" * 50)

        for shipping in shipping_types:
            result = calculator.calculate_shipping(package, shipping, 100, "regular")
            if result["cost"] is not None:
                print(f"{shipping:25} {result['cost']:8.2f} PLN - {result['info']}")
            else:
                print(f"{shipping:25} NIEDOSTĘPNE - {result['info']}")