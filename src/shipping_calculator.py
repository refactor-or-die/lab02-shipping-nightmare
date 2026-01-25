from abc import ABC, abstractmethod
import random
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional

class Package:
    """Paczka do wysyłki - bez zmian"""
    def __init__(self, weight: float, dimensions: Tuple[float, float, float], 
                 value: float, is_fragile: bool = False):
        self.weight = weight  # kg
        self.dimensions = dimensions  # (length, width, height) in cm
        self.value = value  # PLN
        self.is_fragile = is_fragile
    
    @property
    def volume(self):
        return self.dimensions[0] * self.dimensions[1] * self.dimensions[2] / 1000000  # m³


# --- STRATEGY INTERFACE ---

class ShippingStrategy(ABC):
    """Interfejs dla wszystkich strategii wysyłki"""
    
    @abstractmethod
    def calculate(self, package: Package, distance: float, customer_type: str) -> Dict:
        pass


# --- CONCRETE STRATEGIES ---

class StandardShippingStrategy(ShippingStrategy):
    def calculate(self, package: Package, distance: float, customer_type: str) -> Dict:
        base_cost = 15
        
        # Waga
        if package.weight > 20:
            base_cost += (package.weight - 20) * 5
        elif package.weight > 10:
            base_cost += (package.weight - 10) * 3
        elif package.weight > 5:
            base_cost += (package.weight - 5) * 2
            
        # Wymiary
        if package.volume > 0.1:
            base_cost += 20
            
        # Dystans
        if distance > 100:
            base_cost += (distance - 100) * 0.1
            
        # Rabat
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


class ExpressShippingStrategy(ShippingStrategy):
    def calculate(self, package: Package, distance: float, customer_type: str) -> Dict:
        base_cost = 30
        
        if package.weight > 15:
            return self._error("Express nie obsługuje paczek powyżej 15kg")
        
        if package.weight > 8:
            base_cost += (package.weight - 3) * 4 + (package.weight - 8) * 6
        elif package.weight > 3:
            base_cost += (package.weight - 3) * 4
            
        base_cost += distance * 0.2
        
        if package.is_fragile:
            base_cost += 15
            
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

    def _error(self, msg):
        return {"cost": None, "delivery_date": None, "info": msg}


class SameDayShippingStrategy(ShippingStrategy):
    def calculate(self, package: Package, distance: float, customer_type: str) -> Dict:
        if distance > 50:
            return {"cost": None, "delivery_date": None, "info": "Same day delivery dostępne tylko do 50km"}
            
        base_cost = 50
        
        if package.weight > 10:
            return {"cost": None, "delivery_date": None, "info": "Same day nie obsługuje paczek powyżej 10kg"}
        elif package.weight > 5:
            base_cost += 30
            
        if datetime.now().hour > 14:
            base_cost += 20
            
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
        base_cost = 10
        
        if package.is_fragile:
            return {"cost": None, "delivery_date": None, "info": "Economy nie obsługuje przesyłek delikatnych"}
            
        if package.weight < 1:
            base_cost = 8
        else:
            base_cost += package.weight * 1.5
            
        if distance > 500:
            base_cost *= 0.8
            
        delivery_days = random.randint(5, 10)
        
        return {
            "cost": round(base_cost, 2),
            "delivery_date": datetime.now() + timedelta(days=delivery_days),
            "info": "Ekonomiczna dostawa (5-10 dni)"
        }


class InternationalStandardStrategy(ShippingStrategy):
    def calculate(self, package: Package, distance: float, customer_type: str) -> Dict:
        base_cost = 45
        
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
            
        if customer_type == "vip":
            base_cost *= 0.7
        elif customer_type == "premium":
            base_cost *= 0.85
            
        return {
            "cost": round(base_cost, 2),
            "delivery_date": datetime.now() + timedelta(days=delivery_days),
            "info": f"Dostawa międzynarodowa ({zone}) - cło wliczone"
        }


class DroneShippingStrategy(ShippingStrategy):
    def calculate(self, package: Package, distance: float, customer_type: str) -> Dict:
        if package.weight > 2:
            return {"cost": None, "delivery_date": None, "info": "Drony obsługują tylko paczki do 2kg"}
            
        if distance > 20:
            return {"cost": None, "delivery_date": None, "info": "Zasięg dronów to maksymalnie 20km"}
            
        base_cost = 40
        
        weather_penalty = random.choice([0, 10, 20, 50])
        if weather_penalty == 50:
            return {"cost": None, "delivery_date": None, "info": "Złe warunki pogodowe - drony nie latają"}
        
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
            return {"cost": None, "delivery_date": None, "info": "Paczkomaty obsługują maksymalnie 25kg"}
            
        max_dim = max(package.dimensions)
        if max_dim > 60:
            return {"cost": None, "delivery_date": None, "info": "Paczka za duża do paczkomatu"}
            
        base_cost = 12
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


# --- CONTEXT ---

class ShippingCalculator:
    """
    Kalkulator kosztów wysyłki.
    Refaktoryzacja: Strategy Pattern zaimplementowany.
    """
    
    def __init__(self):
        # Rejestracja dostępnych strategii
        self._strategies: Dict[str, ShippingStrategy] = {
            "standard": StandardShippingStrategy(),
            "express": ExpressShippingStrategy(),
            "same_day": SameDayShippingStrategy(),
            "economy": EconomyShippingStrategy(),
            "international_standard": InternationalStandardStrategy(),
            "drone": DroneShippingStrategy(),
            "locker": LockerShippingStrategy()
        }
    
    def calculate_shipping(self, package: Package, shipping_type: str, 
                         distance: float, customer_type: str = "regular") -> Dict:
        """
        Deleguje obliczenia do odpowiedniej strategii.
        """
        strategy = self._strategies.get(shipping_type)
        
        if not strategy:
            return {
                "cost": None,
                "delivery_date": None,
                "info": f"Nieznany typ dostawy: {shipping_type}"
            }
            
        return strategy.calculate(package, distance, customer_type)


# --- EXAMPLE USAGE ---

if __name__ == "__main__":
    calculator = ShippingCalculator()
    
    small_package = Package(0.5, (20, 15, 10), 50)
    medium_package = Package(5, (40, 30, 20), 200, is_fragile=True)
    large_package = Package(15, (60, 50, 40), 500)
    
    shipping_types = ["standard", "express", "same_day", "economy", 
                     "international_standard", "drone", "locker"]
    
    print("=== KALKULATOR KOSZTÓW WYSYŁKI (STRATEGY PATTERN) ===\n")
    
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