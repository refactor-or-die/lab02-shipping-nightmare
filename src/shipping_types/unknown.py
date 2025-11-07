from src.package import Package
from src.shipping_type import ShippingType


class Unknown(ShippingType):
    def calculate(self, package: Package, distance: float, customer_type: str) -> dict:
        # Nieznany typ dostawy
        return {
            "cost": None,
            "delivery_date": None,
            "info": "Nieznany typ dostawy"
        }