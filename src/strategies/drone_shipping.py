from datetime import datetime, timedelta
from random import random
from typing import Dict

from src.strategies.shipping_strategy import ShippingStrategy

from src.models.package import Package


class DroneShipping(ShippingStrategy):
    BASE_RATE = 40

    def calculate(self, package: Package, distance: float, customer_type: str = "regular") -> Dict:
        base_cost = self.BASE_RATE

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