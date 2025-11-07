from datetime import datetime
from typing import Dict

from src.models.package import Package
from src.strategies.shipping_strategy import ShippingStrategy


#MOZE NIE DZIALAC CHODZI O LOGIKE PACZEK >10 kg!!!

class SameDayShipping(ShippingStrategy):
    BASE_RATE = 50

    def shipping(self, package: Package, shipping_type: str, distance: float, customer_type: str = "regular") -> Dict:
        base_cost = self.BASE_RATE
        if distance > 50:
            return {"cost": None, "delivery_date": None, "info": "Same day tylko do 50km"}

        if package.weight > 10:
            return {"cost": None, "delivery_date": None, "info": "Same day nie obsługuje paczek >10kg"}

        if package.weight > 5:
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
