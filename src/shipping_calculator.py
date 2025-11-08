from typing import Tuple, Union
from enum import Enum
import src.shipping_strategy as strategy


class ShippingType(Enum):
    STANDARD = "standard"
    EXPRESS = "express"
    SAME_DAY = "same_day"
    ECONOMY = "economy"
    INTERNATIONAL_STANDARD = "international_standard"
    DRONE = "drone"
    LOCKER = "locker"


class Package:
    """Package for shipping"""

    def __init__(self, weight: float, dimensions: Tuple[float, float, float],
                 value: float, is_fragile: bool = False):
        self.weight = weight  # kg
        self.dimensions = dimensions  # (length, width, height) in cm
        self.value = value  # PLN
        self.is_fragile = is_fragile

    @property
    def volume(self):
        # m³
        return self.dimensions[0] * self.dimensions[1] * self.dimensions[2] / 1000000


class ShippingCalculator:
    """
    Shipping cost calculator.
    Refactored using Strategy Pattern with Enum support!
    """

    def __init__(self):
        # Use enum keys for type safety
        self.strategies = {
            ShippingType.STANDARD: strategy.StandardShipping(),
            ShippingType.EXPRESS: strategy.ExpressShipping(),
            ShippingType.SAME_DAY: strategy.SameDayShipping(),
            ShippingType.DRONE: strategy.DroneShipping(),
            ShippingType.ECONOMY: strategy.EconomyShipping(),
            ShippingType.INTERNATIONAL_STANDARD: strategy.InternationalStandardShipping(),
            ShippingType.LOCKER: strategy.LockerShipping()
        }

    def _normalize_shipping_type(self, shipping_type: Union[str, ShippingType]) -> ShippingType:
        """Convert string to enum for backward compatibility"""
        if isinstance(shipping_type, str):
            try:
                return ShippingType(shipping_type)
            except ValueError:
                return None
        return shipping_type

    def calculate_shipping(self, package, shipping_type: Union[str, ShippingType], distance, customer_type="regular"):
        """
        Args:
            package: Package to ship
            shipping_type: Either a string ("standard") or ShippingType.STANDARD
            distance: Distance in km
            customer_type: "regular", "premium", or "vip"
        """
        normalized_type = self._normalize_shipping_type(shipping_type)

        if normalized_type is None:
            return {"cost": None, "delivery_date": None, "info": f"Unknown delivery type: {shipping_type}"}

        shipping_strategy = self.strategies.get(normalized_type)
        if shipping_strategy:
            return shipping_strategy.calculate(package, distance, customer_type)
        else:
            return {"cost": None, "delivery_date": None, "info": f"Unknown delivery type: {shipping_type}"}


# Example usage
if __name__ == "__main__":
    calculator = ShippingCalculator()

    # Test packages
    small_package = Package(0.5, (20, 15, 10), 50)
    medium_package = Package(5, (40, 30, 20), 200, is_fragile=True)
    large_package = Package(15, (60, 50, 40), 500)

    print("=== SHIPPING COST CALCULATOR ===\n")

    for package, desc in [(small_package, "Small package"),
                          (medium_package, "Medium (fragile)"),
                          (large_package, "Large package")]:
        print(f"\n{desc}: {package.weight}kg, {package.value} units")
        print("-" * 50)

        # Iterate through all enum values
        for shipping_type in ShippingType:
            result = calculator.calculate_shipping(
                package, shipping_type, 100, "regular")
            if result["cost"] is not None:
                print(f"{shipping_type.value:25} {
                      result['cost']:8.2f} units - {result['info']}")
            else:
                print(
                    f"{shipping_type.value:25} UNAVAILABLE - {result['info']}")

    # Backward compatibility: strings still work
    print("\n\n" + "=" * 60)
    print("Demo: Backward compatibility - strings still work")
    print("=" * 60 + "\n")

    result = calculator.calculate_shipping(
        small_package, "standard", 50)  # String
    print(f"String 'standard': {result['cost']} units")

    result = calculator.calculate_shipping(
        small_package, ShippingType.STANDARD, 50)  # Enum
    print(f"Enum ShippingType.STANDARD: {result['cost']} units")
    print("\nBoth produce the same result!")
