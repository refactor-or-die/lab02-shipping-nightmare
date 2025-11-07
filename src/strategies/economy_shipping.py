from datetime import datetime, timedelta
from random import random
from typing import Dict

from src.strategies.shipping_strategy import ShippingStrategy
from src.models.package import Package


class EconomyShipping(ShippingStrategy):
    BASE_RATE = 10

    def shipping(self, package: Package, shipping_type: str, distance: float, customer_type: str = "regular") -> Dict:
        base_cost = self.BASE_RATE

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
