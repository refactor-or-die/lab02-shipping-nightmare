from datetime import datetime, timedelta
from typing import Dict
from src.strategies.shipping_strategy import ShippingStrategy
from src.models.package import Package


class StandardShipping(ShippingStrategy):
    BASE_RATE = 15

    def calculate(self, package: Package, distance: float, customer_type: str = "regular") -> Dict:
        base_cost = self.BASE_RATE

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