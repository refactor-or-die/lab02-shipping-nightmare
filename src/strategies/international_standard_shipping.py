from datetime import datetime, timedelta
from typing import Dict

from src.models.package import Package
from src.strategies.shipping_strategy import ShippingStrategy


class InternationalShipping(ShippingStrategy):
    BASE_RATE =  45

    def shipping(self, package: Package, shipping_type: str, distance: float, customer_type: str = "regular") -> Dict:
        base_cost = self.BASE_RATE

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
