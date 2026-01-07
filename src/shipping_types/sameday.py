from datetime import datetime

from ..shipping_type import ShippingType
from ..shipping_calculator import Package


class SameDay(ShippingType):
    def calculate(self, package: Package, distance: float, customer_type: str) -> dict:
        # Same day tylko do 50km
        if distance > 50:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Same day delivery dostępne tylko do 50km"
            }

        base_cost = 50

        # Same day ma stałą opłatę za wagę
        if package.weight > 5:
            base_cost += 30
        elif package.weight > 10:
            return {
                "cost": None,
                "delivery_date": None,
                "info": "Same day nie obsługuje paczek powyżej 10kg"
            }

        # Dodatkowa opłata za porę dnia
        current_hour = datetime.now().hour
        if current_hour > 14:
            base_cost += 20  # Po 14:00 drożej

        # VIP ma darmową dostawę same day!
        if customer_type == "vip":
            base_cost = 0
        elif customer_type == "premium":
            base_cost *= 0.7

        return {
            "cost": round(base_cost, 2),
            "delivery_date": datetime.now(),
            "info": "Dostawa tego samego dnia!"
        }