import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from abc import ABC, abstractmethod

class Package:
    """Paczka do wysyłki"""
    def __init__(self, weight: float, dimensions: Tuple[float, float, float], 
                 value: float, is_fragile: bool = False):
        self.weight = weight 
        self.dimensions = dimensions 
        self.value = value 
        self.is_fragile = is_fragile
    
    @property
    def volume(self):
        return self.dimensions[0] * self.dimensions[1] * self.dimensions[2] / 1000000 

class ShippingStrategy(ABC):
    @abstractmethod
    def calculate_shipping(self, package: Package, distance: float, customer_type: str = "regular") -> Dict:
        pass


class Standard(ShippingStrategy):
    BASE_RATE = 15 

    def calculate_shipping(self, package: Package, distance: float, customer_type: str = "regular") -> Dict:
        base_cost = self.BASE_RATE
        
        if package.weight > 20:
            base_cost += (package.weight - 20) * 5
        elif package.weight > 10:
            base_cost += (package.weight - 10) * 3
        elif package.weight > 5:
            base_cost += (package.weight - 5) * 2
            
        if package.volume > 0.1:
            base_cost += 20
            
        if distance > 100:
            base_cost += (distance - 100) * 0.1
            
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

class Express(ShippingStrategy):
    BASE_RATE = 30

    def calculate_shipping(self, package: Package, distance: float, customer_type: str = "regular") -> Dict:
        base_cost = self.BASE_RATE
        if package.weight > 15:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Express nie obsługuje paczek powyżej 15kg"
            }
        
        if package.weight > 8:
            base_cost += (package.weight - 8) * 6 + (5 * 4) 
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

class SameDay(ShippingStrategy):
    BASE_RATE = 50 

    def calculate_shipping(self, package: Package, distance: float, customer_type: str = "regular") -> Dict:
        if distance > 50:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Same day delivery dostępne tylko do 50km"
            }
            
        base_cost = self.BASE_RATE
        
        if package.weight > 10:
             return {
                "cost": None,
                "delivery_date": None,
                "info": "Same day nie obsługuje paczek powyżej 10kg"
            }
        elif package.weight > 5:
            base_cost += 30
            
            
        current_hour = datetime.now().hour
        if current_hour > 14:
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

class Economy(ShippingStrategy):
    BASE_RATE = 10 

    def calculate_shipping(self, package: Package, distance: float, customer_type: str="regular") ->Dict:
        base_cost = self.BASE_RATE
        
        if package.weight < 1:
            base_cost = 8
        else:
            base_cost += package.weight * 1.5
            
        if package.is_fragile:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Economy nie obsługuje przesyłek delikatnych"
            }
            
        if distance > 500:
            base_cost *= 0.8
            
        delivery_days = random.randint(5, 10)
        
        return {
            "cost": round(base_cost, 2),
            "delivery_date": datetime.now() + timedelta(days=delivery_days),
            "info": f"Ekonomiczna dostawa (5-10 dni)"
        }

class InternationalStandard(ShippingStrategy):
    BASE_RATE = 45

    def calculate_shipping(self, package: Package, distance: float, customer_type: str="regular") ->Dict:
        base_cost = self.BASE_RATE
        
        customs = package.value * 0.23 if package.value > 150 else 0
        base_cost += customs
        
        if package.weight > 20:
            base_cost += (package.weight - 20) * 12 + (18 * 8) 
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

class Drone(ShippingStrategy):
    BASE_RATE = 40 

    def calculate_shipping(self, package: Package, distance: float, customer_type: str="regular") ->Dict:
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
            
        base_cost = self.BASE_RATE
        
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

class Locker(ShippingStrategy):
    BASE_RATE = 12 
    def calculate_shipping(self, package: Package, distance: float, customer_type: str="regular") ->Dict:
        base_cost = self.BASE_RATE
        
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
    """Kontekst, który używa jednej z klas strategii do obliczenia kosztów"""
    
    def __init__(self):
        self.strategies: Dict[str, ShippingStrategy] = {
            "standard": Standard(),
            "express": Express(),
            "same_day": SameDay(),
            "economy": Economy(),
            "international_standard": InternationalStandard(),
            "drone": Drone(),
            "locker": Locker()
        }
        
    def calculate_shipping(self, package: Package, shipping_type: str, distance: float, customer_type: str = "regular") -> Dict:
        strategy = self.strategies.get(shipping_type)
        if not strategy:
            return {
                "cost": None,
                "delivery_date": None,
                "info": f"Nieznany typ dostawy: {shipping_type}"
            }
        
        return strategy.calculate_shipping(package, distance, customer_type)

            
if __name__ == "__main__":
    calculator = ShippingCalculator()
    
    small_package = Package(0.5, (20, 15, 10), 50)
    medium_package = Package(5, (40, 30, 20), 200, is_fragile=True)
    large_package = Package(15, (60, 50, 40), 500)
    
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