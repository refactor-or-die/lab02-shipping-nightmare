from datetime import datetime, timedelta
import random

from ..shipping_type import ShippingType
from ..shipping_calculator import Package

class Economy(ShippingType):
    def calculate(self, package: Package, distance: float, customer_type: str) -> dict:
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

