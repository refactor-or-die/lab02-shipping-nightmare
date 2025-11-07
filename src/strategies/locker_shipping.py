from datetime import datetime, timedelta
from typing import Dict

from src.models.package import Package
from src.strategies.shipping_strategy import ShippingStrategy


class LockerShipping(ShippingStrategy):
    BASE_RATE = 12

    def shipping(self, package: Package, shipping_type: str, distance: float, customer_type: str = "regular") -> Dict:
        base_cost = self.BASE_RATE

        # Paczkomaty mają limity
        if package.weight > 25:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Paczkomaty obsługują maksymalnie 25kg"
            }

        # Sprawdzenie wymiarów
        max_dim = max(package.dimensions)
        if max_dim > 60:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Paczka za duża do paczkomatu"
            }

        # Stała opłata niezależnie od wagi
        if distance > 50:
            base_cost += 3

        # VIP ma darmowe paczkomaty
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