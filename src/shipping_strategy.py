import src.shipping_calculator as sc
from datetime import datetime, timedelta
from typing import Dict
from abc import ABC, abstractmethod
import random


class ShippingStrategy(ABC):
    """Abstract base class for shipping strategies"""

    @abstractmethod
    def calculate(self, package: sc.Package, distance: float, customer_type: str = "regular") -> Dict:
        """Calculate shipping cost for a package"""
        pass


class StandardShipping(ShippingStrategy):
    def __init__(self):
        self.base_rate = 15

    def calculate(self, package, distance, customer_type="regular"):
        base_cost = self.base_rate

        # Additional weight fees
        if package.weight > 5:
            base_cost += (package.weight - 5) * 2
        elif package.weight > 10:
            base_cost += (package.weight - 10) * 3
        elif package.weight > 20:
            base_cost += (package.weight - 20) * 5

        # Dimension fee
        if package.volume > 0.1:
            base_cost += 20

        # Distance fee
        if distance > 100:
            base_cost += (distance - 100) * 0.1

        # Customer discount
        if customer_type == "premium":
            base_cost *= 0.9
        elif customer_type == "vip":
            base_cost *= 0.8

        delivery_days = 3 if distance < 200 else 5

        return {
            "cost": round(base_cost, 2),
            "delivery_date": datetime.now() + timedelta(days=delivery_days),
            "info": "Standard courier delivery"
        }


class ExpressShipping(ShippingStrategy):
    def __init__(self):
        self.base_rate = 30

    def calculate(self, package, distance, customer_type="regular"):
        base_cost = self.base_rate

        # Express doesn't accept packages over 15kg
        if package.weight > 15:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Express doesn't handle packages over 15kg"
            }

        # Express has different weight thresholds
        if package.weight > 8:
            base_cost += (package.weight - 3) * 4 + (package.weight - 8) * 6
        elif package.weight > 3:
            base_cost += (package.weight - 3) * 4

        # Express has higher distance fee
        base_cost += distance * 0.2

        # Fragile package fee
        if package.is_fragile:
            base_cost += 15

        # Discounts
        if customer_type == "premium":
            base_cost *= 0.95
        elif customer_type == "vip":
            base_cost *= 0.85

        delivery_days = 1 if distance < 300 else 2

        return {
            "cost": round(base_cost, 2),
            "delivery_date": datetime.now() + timedelta(days=delivery_days),
            "info": "Express delivery - priority"
        }


class SameDayShipping(ShippingStrategy):
    def __init__(self):
        self.base_rate = 50

    def calculate(self, package, distance, customer_type="regular"):
        # Same day only up to 50km
        if distance > 50:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Same day delivery available only up to 50km"
            }

        base_cost = self.base_rate

        # Same day has fixed weight fee
        if package.weight > 5:
            base_cost += 30
        elif package.weight > 10:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Same day doesn't handle packages over 10kg"
            }

        # Additional fee for time of day
        current_hour = datetime.now().hour
        if current_hour > 14:
            base_cost += 20  # More expensive after 2 PM

        # VIP gets free same day delivery!
        if customer_type == "vip":
            base_cost = 0
        elif customer_type == "premium":
            base_cost *= 0.7

        return {
            "cost": round(base_cost, 2),
            "delivery_date": datetime.now(),
            "info": "Same day delivery!"
        }


class DroneShipping(ShippingStrategy):
    def __init__(self):
        self.base_rate = 40

    def calculate(self, package, distance, customer_type="regular"):
        # Drone delivery - the future!
        if package.weight > 2:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Drones only handle packages up to 2kg"
            }

        if distance > 20:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Drone range is maximum 20km"
            }

        base_cost = self.base_rate

        # Weather conditions (simulation)
        weather_penalty = random.choice([0, 10, 20, 50])
        if weather_penalty == 50:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Bad weather conditions - drones don't fly"
            }

        base_cost += weather_penalty

        # Premium and VIP have priority
        if customer_type in ["premium", "vip"]:
            base_cost *= 0.5
            delivery_time = 30  # minutes
        else:
            delivery_time = 60  # minutes

        return {
            "cost": round(base_cost, 2),
            "delivery_date": datetime.now() + timedelta(minutes=delivery_time),
            "info": f"Drone delivery in {delivery_time} minutes!"
        }


class EconomyShipping(ShippingStrategy):
    def __init__(self):
        self.base_rate = 10

    def calculate(self, package, distance, customer_type="regular"):
        base_cost = self.base_rate

        # Economy has minimum fee
        if package.weight < 1:
            base_cost = 8
        else:
            base_cost += package.weight * 1.5

        # We don't deliver fragile packages via economy
        if package.is_fragile:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Economy doesn't handle fragile packages"
            }

        # The farther, the cheaper (bulk transport)
        if distance > 500:
            base_cost *= 0.8

        # No discounts for economy
        delivery_days = random.randint(5, 10)  # Unpredictable time

        return {
            "cost": round(base_cost, 2),
            "delivery_date": datetime.now() + timedelta(days=delivery_days),
            "info": f"Economy delivery (5-10 days)"
        }


class InternationalStandardShipping(ShippingStrategy):
    def __init__(self):
        self.base_rate = 45

    def calculate(self, package, distance, customer_type="regular"):
        base_cost = self.base_rate

        # Simulated customs fees
        customs = package.value * 0.23 if package.value > 150 else 0
        base_cost += customs

        # International weight
        if package.weight > 2:
            base_cost += (package.weight - 2) * 8
        elif package.weight > 20:
            base_cost += (package.weight - 20) * 12

        # Delivery zone
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

        # International discounts
        if customer_type == "vip":
            base_cost *= 0.7
        elif customer_type == "premium":
            base_cost *= 0.85

        return {
            "cost": round(base_cost, 2),
            "delivery_date": datetime.now() + timedelta(days=delivery_days),
            "info": f"International delivery ({zone}) - customs included"
        }


class LockerShipping(ShippingStrategy):
    def __init__(self):
        self.base_rate = 12

    def calculate(self, package, distance, customer_type="regular"):
        base_cost = self.base_rate

        # Lockers have limits
        if package.weight > 25:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Lockers handle maximum 25kg"
            }

        # Check dimensions
        max_dim = max(package.dimensions)
        if max_dim > 60:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Package too large for locker"
            }

        # Fixed fee regardless of weight
        if distance > 50:
            base_cost += 3

        # VIP gets free lockers
        if customer_type == "vip":
            base_cost = 0
        elif customer_type == "premium":
            base_cost *= 0.8

        delivery_days = 1 if distance < 200 else 2

        return {
            "cost": round(base_cost, 2),
            "delivery_date": datetime.now() + timedelta(days=delivery_days),
            "info": "Delivery to locker"
        }
