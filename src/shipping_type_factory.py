from shipping_type import *

class ShippingTypeFactory():
    def create(self, shipping_type: str) -> ShippingType:
        match shipping_type:
            case "standard":
                return StandardShipping()
            case "express":
                return ExpressShipping()
            case "same_day":
                return SameDayShipping()
            case "economy":
                return EconomyShipping()
            case "international_standard":
                return InternationalStandardShipping()
            case "drone":
                return DroneShipping()
            case "locker":
                return LockerShipping()
            case _:
                return UnknownShipping()
