from datetime import datetime, timedelta
from typing import Dict

from src.models.package import Package
from src.strategies.shipping_strategy import ShippingStrategy


class ExpressShipping(ShippingStrategy):
    BASE_RATE = 30

    def calculate(self, package: Package, distance: float, customer_type: str = "regular") -> Dict:
        base_cost = self.BASE_RATE

        if package.weight > 15:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Express nie obsługuje paczek powyżej 15kg"
            }

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

